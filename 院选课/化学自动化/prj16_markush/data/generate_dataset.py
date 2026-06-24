import json
import re
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D


ROOT = Path(__file__).resolve().parent
IMAGE_DIR = ROOT / "images"
WIDTH = 400
HEIGHT = 300


STANDARD_MOLECULES = [
    ("A001", "benzene", "Benzene", "c1ccccc1"),
    ("A002", "aspirin", "Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
    ("A003", "caffeine", "Caffeine", "Cn1cnc2c1c(=O)n(C)c(=O)n2C"),
    ("A004", "ethanol", "Ethanol", "CCO"),
    ("A005", "glucose", "Glucose", "C(C1C(C(C(C(O1)O)O)O)O)O"),
    ("A006", "paracetamol", "Paracetamol", "CC(=O)Nc1ccc(O)cc1"),
    ("A007", "dopamine", "Dopamine", "NCCc1ccc(O)c(O)c1"),
    ("A008", "ibuprofen", "Ibuprofen", "CC(C)Cc1ccc(C(C)C(=O)O)cc1"),
]

MARKUSH_MOLECULES = [
    ("B001", "phenyl_R", "Phenyl with R group", "c1ccc(*)cc1", ["R"]),
    ("B002", "phenyl_R1", "Phenyl with R1 group", "c1ccc(*)cc1", ["R1"]),
    ("B003", "phenyl_R2", "Phenyl with R2 group", "c1ccc(*)cc1", ["R2"]),
    ("B004", "disubstituted_phenyl_R_R1", "Disubstituted phenyl with R and R1", "c1cc(*)ccc1*", ["R", "R1"]),
    ("B005", "anisole_R", "Anisole with R group", "COc1ccc(*)cc1", ["R"]),
    ("B006", "benzoic_acid_R", "Benzoic acid with R group", "O=C(O)c1ccc(*)cc1", ["R"]),
    ("B007", "ethyl_R", "Ethyl chain with R group", "CC*", ["R"]),
    ("B008", "amide_R", "Amide with R group", "CC(=O)N*", ["R"]),
    ("B009", "pyridine_R", "Pyridine with R group", "n1cc(*)ccc1", ["R"]),
    ("B010", "cyclohexyl_R_R2", "Cyclohexyl with R and R2", "C1CC(*)CCC1*", ["R", "R2"]),
    ("C001", "chain_A", "Chain with A substituent", "CCC*", ["A"]),
    ("C002", "phenyl_X", "Phenyl with X atom", "c1ccc(*)cc1", ["X"]),
    ("C003", "phenyl_Z", "Phenyl with Z atom", "c1cc(*)ccc1", ["Z"]),
    ("C004", "chain_A_X", "Chain with A and X substituents", "*CC*", ["A", "X"]),
    ("C005", "heteroaryl_A", "Heteroaryl with A substituent", "n1cc(*)ccc1", ["A"]),
    ("C006", "generic_A_Z", "Aromatic ring with A and Z", "c1cc(*)c(*)cc1", ["A", "Z"]),
    ("C007", "variable_chain_n", "Variable-length alkyl chain", "CCCCC", ["n=1-4"]),
]

COMPLEX_MARKUSH_MOLECULES = [
    ("D001", "phenyl_R_alkyl_aryl", "Phenyl R substituent: alkyl or aryl", "*c1ccccc1", ["R"], "substituent_variation", "R=alkyl/aryl"),
    ("D002", "anisole_R_halogen", "Anisole R substituent: F, Cl, Br, or I", "COc1ccc(*)cc1", ["R"], "substituent_variation", "R=F/Cl/Br/I"),
    ("D003", "anilide_R_heteroaryl", "Anilide R substituent: heteroaryl group", "CC(=O)Nc1ccc(*)cc1", ["R"], "substituent_variation", "R=heteroaryl"),
    ("D004", "benzoic_acid_R_acyl", "Benzoic acid R substituent: acyl group", "O=C(O)c1ccc(*)cc1", ["R"], "substituent_variation", "R=acyl"),
    ("D005", "pyridine_R_alkoxy", "Pyridine R substituent: alkoxy group", "*c1ccncc1", ["R"], "substituent_variation", "R=alkoxy"),
    ("D006", "amide_N_R1_R2", "Amide nitrogen substituent variation R1/R2", "CC(=O)N(*)*", ["R1", "R2"], "substituent_variation", "R1/R2 variable"),
    ("D007", "urea_R1_R2", "Urea substituent variation R1/R2", "NC(=O)N(*)*", ["R1", "R2"], "substituent_variation", "R1/R2 variable"),
    ("D008", "sulfone_R_aryl", "Sulfone R substituent: aryl or heteroaryl", "CS(=O)(=O)*", ["R"], "substituent_variation", "R=aryl/heteroaryl"),
    ("D009", "ortho_chloro_phenyl_R", "Ortho-position R variation on chlorophenyl", "Clc1ccccc1*", ["R"], "position_variation", "o-R"),
    ("D010", "meta_chloro_phenyl_R", "Meta-position R variation on chlorophenyl", "Clc1cc(*)ccc1", ["R"], "position_variation", "m-R"),
    ("D011", "para_chloro_phenyl_R", "Para-position R variation on chlorophenyl", "Clc1ccc(*)cc1", ["R"], "position_variation", "p-R"),
    ("D012", "pyridine_2_R", "Pyridine 2-position R variation", "*c1ccccn1", ["R"], "position_variation", "2-R"),
    ("D013", "pyridine_3_R", "Pyridine 3-position R variation", "*c1cccnc1", ["R"], "position_variation", "3-R"),
    ("D014", "pyridine_4_R", "Pyridine 4-position R variation", "*c1ccncc1", ["R"], "position_variation", "4-R"),
    ("D015", "naphthyl_alpha_R", "Alpha-naphthyl R position variation", "*c1cccc2ccccc12", ["R"], "position_variation", "alpha-R"),
    ("D016", "naphthyl_beta_R", "Beta-naphthyl R position variation", "*c1ccc2ccccc2c1", ["R"], "position_variation", "beta-R"),
    ("D017", "phenyl_mono_R", "Phenyl frequency variation mono R", "*c1ccccc1", ["R"], "frequency_variation", "x=1"),
    ("D018", "phenyl_di_R", "Phenyl frequency variation di R", "*c1ccc(*)cc1", ["R", "R"], "frequency_variation", "x=2"),
    ("D019", "phenyl_tri_R", "Phenyl frequency variation tri R", "*c1cc(*)cc(*)c1", ["R", "R", "R"], "frequency_variation", "x=3"),
    ("D020", "cyclohexyl_di_R", "Cyclohexyl frequency variation di R", "*C1CCC(*)CC1", ["R", "R"], "frequency_variation", "x=2"),
    ("D021", "triazine_tri_R", "Triazine frequency variation tri R", "*c1nc(*)nc(*)n1", ["R", "R", "R"], "frequency_variation", "x=1-3"),
    ("D022", "amide_repeat_m", "Repeating amide frequency variation", "CC(=O)NCC*", ["R"], "frequency_variation", "m=0-3"),
    ("D023", "ethylene_repeat_n", "Ethylene homology variation", "*CCCC*", ["R", "X"], "homology_variation", "n=1-4"),
    ("D024", "alkyl_chain_m", "Alkyl-chain homology variation", "CCCCCC*", ["R"], "homology_variation", "m=1-6"),
    ("D025", "oxyethylene_repeat_n", "Oxyethylene homology variation", "*CCOCC*", ["R", "R1"], "homology_variation", "n=1-5"),
    ("D026", "methylene_spacer_p", "Methylene spacer homology variation", "*CCCC(=O)O", ["R"], "homology_variation", "p=0-4"),
    ("D027", "aryl_linker_q", "Aryl-linker homology variation", "*c1ccc(CC*)cc1", ["R", "X"], "homology_variation", "q=1-3"),
    ("D028", "heteroatom_family_A", "Same-family homology variation A", "*CC(=O)O", ["A"], "homology_variation", "A=O/S/Se"),
    ("D029", "halogen_family_X", "Halogen-family variation X", "*c1ccc(C(=O)O)cc1", ["X"], "substituent_variation", "X=F/Cl/Br/I"),
    ("D030", "combined_R_X_n", "Combined substituent, position, and frequency variation", "*c1cc(*)ccc1CC", ["R", "X"], "frequency_variation", "R/X; n=1-2"),
]


def _prepare_mol(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    AllChem.Compute2DCoords(mol)
    return mol


def draw_standard(smiles, path):
    mol = _prepare_mol(smiles)
    Draw.MolToFile(mol, str(path), size=(WIDTH, HEIGHT), kekulize=True)
    flatten_to_white(path)


def flatten_to_white(path):
    image = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255, 255))
    background.alpha_composite(image)
    background.convert("RGB").save(path)


def mol_to_svg(smiles, labels=None):
    mol = _prepare_mol(smiles)
    drawer = rdMolDraw2D.MolDraw2DSVG(WIDTH, HEIGHT)
    options = drawer.drawOptions()
    options.clearBackground = False
    if labels:
        dummy_atoms = [atom.GetIdx() for atom in mol.GetAtoms() if atom.GetAtomicNum() == 0]
        for atom_idx, label in zip(dummy_atoms, labels):
            options.atomLabels[atom_idx] = label
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def replace_placeholders(svg, labels):
    replacement_iter = iter(labels)

    def repl(match):
        return f">{next(replacement_iter)}<"

    result = re.sub(r">\*<", repl, svg, count=len(labels))
    if ">*<" in result and len(labels) == 0:
        return result
    return result


def draw_markush(smiles, labels, path):
    svg = replace_placeholders(mol_to_svg(smiles, labels), labels)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(path), output_width=WIDTH, output_height=HEIGHT)
    flatten_to_white(path)


def annotate_variable_chain(path, text="n=1-4"):
    flatten_to_white(path)
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((260, 215), text, fill=(0, 0, 0), font=font)
    image.save(path)


def make_metadata_entry(identifier, filename, category, name, expected_smiles, symbols, markush_class=None):
    entry = {
        "id": identifier,
        "filename": f"images/{filename}",
        "category": category,
        "molecule_name": name,
        "expected_smiles": expected_smiles,
        "generic_symbols": symbols,
    }
    if markush_class:
        entry["markush_class"] = markush_class
    return entry


def main():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    metadata = []

    for identifier, slug, name, smiles in STANDARD_MOLECULES:
        filename = f"{identifier}_{slug}.png"
        draw_standard(smiles, IMAGE_DIR / filename)
        metadata.append(make_metadata_entry(identifier, filename, "A", name, smiles, []))

    for identifier, slug, name, smiles, labels in MARKUSH_MOLECULES:
        filename = f"{identifier}_{slug}.png"
        path = IMAGE_DIR / filename
        if identifier == "C007":
            draw_standard(smiles, path)
            annotate_variable_chain(path)
        else:
            draw_markush(smiles, labels, path)
        metadata.append(make_metadata_entry(identifier, filename, identifier[0], name, None, labels))

    for identifier, slug, name, smiles, labels, markush_class, annotation in COMPLEX_MARKUSH_MOLECULES:
        filename = f"{identifier}_{slug}.png"
        path = IMAGE_DIR / filename
        draw_markush(smiles, labels, path)
        annotate_variable_chain(path, annotation)
        metadata.append(make_metadata_entry(identifier, filename, "D", name, None, labels, markush_class))

    metadata_path = ROOT / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(metadata)} records and {len(list(IMAGE_DIR.glob('*.png')))} PNG files.")


if __name__ == "__main__":
    main()
