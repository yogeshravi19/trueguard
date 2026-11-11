# -*- coding: utf-8 -*-
"""
Revision pass R1 for 'submitted for finla rview.docx'.
Always starts from the ORIGINAL file. Produces:
  revision/Manuscript_R1_marked.docx  (all new/rewritten text in blue, placeholders in yellow)
  revision/Manuscript_R1_clean.docx   (same content, black text, placeholders still yellow)
Usage: python revise_r1.py
"""
import copy, re, os, sys
import docx
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = r'E:\trueguard\CAPSTONE\submitted for finla rview.docx'
OUTDIR = r'E:\trueguard\CAPSTONE\revision'
BLUE = RGBColor(0x00, 0x00, 0xFF)

# ----------------------------------------------------------------- helpers
def is_drawing(el):
    return el.find('.//' + qn('w:drawing')) is not None or el.find('.//' + qn('w:pict')) is not None

def first_rpr(p_el):
    for r in p_el.iter(qn('w:r')):
        if not is_drawing(r) and r.find(qn('w:t')) is not None:
            rp = r.find(qn('w:rPr'))
            return copy.deepcopy(rp) if rp is not None else None
    return None

class Editor:
    def __init__(self, doc, mark):
        self.doc, self.mark = doc, mark

    def _make_runs(self, p, text, tmpl, mark):
        """Create run elements for text. **bold**, {{placeholder}} (yellow)."""
        made = []
        for seg in re.split(r'(\{\{.*?\}\}|\*\*.*?\*\*)', text, flags=re.S):
            if not seg:
                continue
            ph = seg.startswith('{{')
            bold = seg.startswith('**')
            if ph or bold:
                seg = seg[2:-2]
            r = p.add_run(seg)
            old = r._r.find(qn('w:rPr'))
            if tmpl is not None:
                if old is not None:
                    r._r.remove(old)
                r._r.insert(0, copy.deepcopy(tmpl))
            if mark:
                r.font.color.rgb = BLUE
            if bold:
                r.bold = True
            if ph:
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r._r.getparent().remove(r._r)
            made.append(r._r)
        return made

    def set_text(self, p, text, mark=None, tmpl=None):
        mark = self.mark if mark is None else mark
        p_el = p._p
        removable = [c for c in p_el if (c.tag == qn('w:r') and not is_drawing(c)) or c.tag == qn('w:hyperlink')]
        if tmpl is None:
            tmpl = first_rpr(p_el)
        new = self._make_runs(p, text, tmpl, mark)
        first = removable[0] if removable else None
        if first is not None:
            for n in new:
                first.addprevious(n)
        else:
            for n in new:
                p_el.append(n)
        for c in removable:
            p_el.remove(c)
        return p

    def new_par_after(self, anchor_el, text, template_p, mark=None):
        el = copy.deepcopy(template_p._p)
        for c in list(el):
            if c.tag != qn('w:pPr'):
                el.remove(c)
        anchor_el.addnext(el)
        np_ = Paragraph(el, template_p._parent)
        self.set_text(np_, text, mark=mark, tmpl=first_rpr(template_p._p))
        return np_

    def restyle_like(self, p, like_p):
        old = p._p.find(qn('w:pPr'))
        if old is not None:
            p._p.remove(old)
        p._p.insert(0, copy.deepcopy(like_p._p.find(qn('w:pPr'))))

    @staticmethod
    def delete(p):
        el = p._p
        el.getparent().remove(el)

    def build_table(self, rows, like_tbl, mark=None, highlight_cells=()):
        mark = self.mark if mark is None else mark
        t = self.doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = like_tbl.style
        hdr_tmpl = first_rpr(like_tbl.rows[0].cells[0].paragraphs[0]._p)
        body_tmpl = first_rpr(like_tbl.rows[1].cells[0].paragraphs[0]._p)
        hdr_shd = like_tbl.rows[0].cells[0]._tc.find('.//' + qn('w:shd'))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.rows[i].cells[j]
                para = cell.paragraphs[0]
                ref_par = like_tbl.rows[min(i, 1)].cells[0].paragraphs[0]
                if ref_par._p.find(qn('w:pPr')) is not None:
                    self.restyle_like(para, ref_par)
                txt = f'**{val}**' if i == 0 else val
                self.set_text(para, txt, mark=mark, tmpl=hdr_tmpl if i == 0 else body_tmpl)
                if i == 0 and hdr_shd is not None:
                    tcPr = cell._tc.get_or_add_tcPr()
                    tcPr.append(copy.deepcopy(hdr_shd))
        return t

def expect(P, i, snippet):
    got = P[i].text.strip()
    if not got.startswith(snippet):
        raise SystemExit(f'Index check failed at P{i}: expected "{snippet}", got "{got[:60]}"')

# ----------------------------------------------------------------- content
from revise_r1_text import TEXT, METHODS, REFS, TABLES, TRUEGUARD

def run(mark):
    doc = docx.Document(SRC)
    E = Editor(doc, mark)
    P = list(doc.paragraphs)
    T = list(doc.tables)

    checks = {11: 'Large Language Models (LLMs) have demonstrated', 12: 'trustworthy use', 13: 'Keywords',
              16: 'Over the last', 34: 'Figure 1', 48: 'All these', 49: 'It is our effort', 54: 'The rest',
              57: 'The twenty', 60: 'The intuition', 66: 'HALLUSHIFT+', 68: 'hallucination happens',
              72: 'This is where', 82: 'Entropy Production', 83: 'invoking', 91: 'LLM Check', 93: 'They multiply',
              100: 'Figure 5', 101: 'Calibration', 121: 'Figure 6', 122: 'Explanation framing', 130: 'The Complementarity',
              140: 'Where Are', 142: 'Table 1', 168: 'Figure 8', 169: 'Speedup', 188: 'TRUEGUARD', 189: 'The gaps',
              190: '(Trustworthy', 191: 'multi signal', 192: 'Figure 9', 193: 'Multi Signal', 195: 'Distribution Shift',
              196: 'Figure 10', 197: 'AUROC versus', 201: 'Learner', 204: 'Closed Loop', 212: 'Figure 12',
              216: 'Retrieval augmented', 220: 'Evaluation of Trust', 224: 'We wrap', 226: 'Online', 229: 'The field',
              233: '7.Data', 235: 'This study', 240: '8.Conflict', 242: 'The authors', 246: '9.Funding', 249: '10.References'}
    for i, s in checks.items():
        expect(P, i, s)

    H1, H2, BODY = P[56], P[59], P[60]

    # ---- 1. simple paragraph rewrites (blue)
    for i, txt in TEXT.items():
        E.set_text(P[i], txt)

    # ---- 2. formatting-only merges (not blue)
    for i, txt in {101: 'Figure 5: Calibration and explainability methods (BehCal RL, Human Trust) yield the largest percentage gains over their respective baselines.',
                   121: 'Figure 6: Explanation framing boosts user trust by 22 percentage points, but only when users can compare outputs.',
                   168: 'Figure 8: Efficiency trade-off: speed-up factor (log scale) versus AUROC. LLM-Check achieves up to 450\u00d7 speed-up.',
                   192: 'Figure 9: Four-panel overview comparing HaluEval AUROC, SEP versus semantic entropy, effectiveness by hallucination type, and improvement over baseline across papers.',
                   196: 'Figure 10: AUROC versus F1 scatter showing SEP and LLM-Check as the best-performing methods.',
                   212: 'Figure 12: BehCal RL achieves the lowest calibration error across three benchmarks without sacrificing task accuracy.',
                   233: 'Data Availability Statement', 240: 'Conflict of Interest Statement', 246: 'Funding', 249: 'References',
                   242: 'The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.',
                   247: 'This research received no external funding.'}.items():
        E.set_text(P[i], txt, mark=False)
    for i in (100, 191):           # image paragraphs: drop stray text, keep image
        E.set_text(P[i], '', mark=False)

    # ---- 3. heading restyles
    for i, title in {130: 'Complementarity of Detection Signals', 133: 'Detection Performance versus Cost',
                     136: 'Model Access and Black-Box Deployment', 138: 'Disconnect Between Detection and Mitigation',
                     140: 'Absence of User-Facing Explanations'}.items():
        E.restyle_like(P[i], H2)
        E.set_text(P[i], title, tmpl=first_rpr(H2._p))
    E.restyle_like(P[188], P[171])
    E.set_text(P[188], 'TRUEGUARD: A Conceptual Closed-Loop Framework', tmpl=first_rpr(P[171]._p))
    for i, title in {180: 'Disconnect Between Detection and Mitigation', 193: 'Sensing: Multi-Signal Detection',
                     201: 'Explanation Module', 204: 'Actuation: Tiered Closed-Loop Mitigation',
                     220: 'Evaluation Protocol for Future Work'}.items():
        E.set_text(P[i], title)

    # ---- 4. new paragraphs inserted after existing ones
    a = E.new_par_after(P[57]._p, TEXT['_taxonomy_rationale'], BODY)
    E.new_par_after(P[83]._p, TEXT['_selfcheck'], BODY)          # (P83 deleted later; insert first)
    E.new_par_after(P[104]._p, TEXT['_benchmarks'], BODY)
    E.new_par_after(P[112]._p, TEXT['_foundational_mitigation'], BODY)
    # Comparative analysis: explanation body + evaluation criteria + comparability
    x = E.new_par_after(P[140]._p, TEXT['_explanations_body'], BODY)
    x = E.new_par_after(x._p, 'Evaluation Criteria Beyond Detection Accuracy', H2)
    x = E.new_par_after(x._p, TEXT['_eval_criteria'], BODY)
    x = E.new_par_after(x._p, TEXT['_comparability'], BODY)

    # ---- 5. Methodology section after P54
    anchor = P[54]._p
    for kind, txt in METHODS:
        if kind == 'TABLE':
            tbl = E.build_table(txt, T[0])
            anchor.addnext(tbl._tbl)
            anchor = tbl._tbl
            continue
        tpl = {'H1': H1, 'H2': H2, 'B': BODY}[kind]
        anchor = E.new_par_after(anchor, txt, tpl)._p

    # ---- 6. Tables: rebuild Table 1 (benchmarks) & Table 2 (mitigation), patch Table 3 (detection)
    for old, key, cap_after in ((T[0], 'benchmarks', P[105]), (T[1], 'mitigation', P[113])):
        new = E.build_table(TABLES[key]['rows'], old)
        old._tbl.addprevious(new._tbl)
        old._tbl.getparent().remove(old._tbl)
        E.new_par_after(cap_after._p, TABLES[key]['caption'], P[142])
    det = T[2]
    for r in det.rows:
        if r.cells[0].text.startswith('Sem. Energy'):
            E.set_text(r.cells[1].paragraphs[0], 'Logit energy')
            E.set_text(r.cells[3].paragraphs[0], 'Multiple samples')
    E.set_text(P[142], TABLES['detection_caption'])

    # ---- 7. TRUEGUARD section
    tg = TRUEGUARD
    x = E.new_par_after(P[189]._p, 'Closed-Loop Structure', H2)
    x = E.new_par_after(x._p, tg['closed_loop'], BODY)
    x = E.new_par_after(x._p, tg['figure_placeholder'], BODY)
    E.set_text(P[194], tg['sensing'])
    E.set_text(P[195], tg['sensing2'])
    x = E.new_par_after(P[196]._p, 'Signal Fusion and Fault Detection', H2)
    for t_ in tg['fusion']:
        x = E.new_par_after(x._p, t_, BODY)
    E.set_text(P[202], tg['explanation'])
    E.set_text(P[205], tg['actuation_intro'])
    E.set_text(P[216], tg['tier12'])
    E.set_text(P[217], tg['tier34'])
    E.set_text(P[218], tg['feedback'])
    x = E.new_par_after(P[218]._p, 'Model Access Modes and Computational Overhead', H2)
    for t_ in tg['access']:
        x = E.new_par_after(x._p, t_, BODY)
    E.set_text(P[221], tg['evaluation'])

    # ---- 8. References: rebuild numbered list
    ref_tpl = P[251]
    tmpl = first_rpr(ref_tpl._p)
    anchor = P[249]._p
    for n, (txt, changed) in enumerate(REFS, 1):
        np_ = E.new_par_after(anchor, f'[{n}] {txt}', ref_tpl, mark=(mark and changed))
        anchor = np_._p
    for p in P[250:]:
        E.delete(p)

    # ---- 9. deletions (merged / obsolete paragraphs)
    for i in [12] + list(range(36, 46)) + [68, 83, 93, 122, 169, 190, 197, 198, 213, 214, 236, 237, 238, 243]:
        E.delete(P[i])

    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, 'Manuscript_R1_marked.docx' if mark else 'Manuscript_R1_clean.docx')
    doc.save(out)
    print('saved', out)

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run(True)
    run(False)
