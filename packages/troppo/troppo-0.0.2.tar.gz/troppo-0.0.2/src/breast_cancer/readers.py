import pandas as pd


# base data from breast cancer
# TODO THIS IS IMPORTANT -> MAKE THIS TO DOWNLOAD THE INFORMATION (SINCE MOST OF THE DATASETS ARE GOING TO TAKE A LOT
# todo ON THE GIT

class BreastCancerOmicsAndInformation():
	def __init__(self):
		self.breast_cancer_information = self.load_breast_cancer_info()
		self.gdsc_data = self.load_gdsc_breast_cancer()
		self.nci_60_data = self.load_nci60_breast_cancer()
		self.hpa_normal_adipocytes_data, self.hpa_normal_glandular_data, self.hpa_normal_myoepithelial = self.load_normal_hpa()

	def __simplify_names(self, cell_line):
		return str(cell_line).upper().replace('-', '')

	def load_breast_cancer_info(self):
		return pd.read_csv('./data/breast_cancer_cell_lines.tsv', sep='\t')

	def load_gdsc_breast_cancer(self):
		# TODO here should be the ability to check if the file is present; if not, download from the website
		gdsc_preprocessed = pd.read_csv('./data/sanger1018_brainarray_ensemblgene_rma.txt',
										sep='\t')
		mapping = pd.read_excel('./data/Cell_Lines_Details.xlsx', dtype={'COSMIC identifier': str}, sheet_name=None)
		mapping_dict = dict(
			zip(mapping['Cell line details']['COSMIC identifier'], mapping['Cell line details']['Sample Name']))
		gdsc_preprocessed_mapped = gdsc_preprocessed.rename(
			columns={k: self.__simplify_names(v) for k, v in mapping_dict.items()})

		# select only the breast cancer data
		cell_lines_to_keep = [c for c in gdsc_preprocessed_mapped.columns if
							  c in self.breast_cancer_information['Cell lines'].tolist()]
		cell_lines_to_keep.append('ensembl_gene')  # to keep the genes for later conversion

		return gdsc_preprocessed_mapped[cell_lines_to_keep]

	def load_nci60_breast_cancer(self):
		nci_60 = pd.read_excel('./data/RNA__Affy_HG_U133_Plus_2.0_RMA.xls')
		breast_cancer_columns = [c for c in nci_60.columns if 'BR:' in c]
		breast_cancer_columns.append('Probe id c')
		breast_cancer_columns.append('Gene name d')

		return nci_60[breast_cancer_columns]

	def load_normal_hpa(self):
		normal_hpa = pd.read_csv('./data/HPA/normal_tissue.tsv', sep='\t')
		normal_hpa_breast = normal_hpa[normal_hpa.Tissue == 'breast']
		normal_hpa_breast_glandular = normal_hpa_breast[normal_hpa_breast['Cell type'] == 'glandular cells']
		normal_hpa_breast_adipocytes = normal_hpa_breast[normal_hpa_breast['Cell type'] == 'adipocytes']
		normal_hpa_breast_myoepithelial = normal_hpa_breast[normal_hpa_breast['Cell type'] == 'myoepithelial cells']

		return normal_hpa_breast_adipocytes, normal_hpa_breast_glandular, normal_hpa_breast_myoepithelial


if __name__ == '__main__':
	# tests
	b = BreastCancerOmicsAndInformation()

	# HPA pathology
	pathology_hpa = pd.read_csv('./data/HPA/pathology.tsv', sep = '\t')
	pathology_hpa_breast_cancer = pathology_hpa[pathology_hpa['Cancer']=='breast cancer']


	# HPA proteinatlas
	protein_atlas_hpa = pd.read_csv('./data/HPA/proteinatlas.tsv', sep = '\t')

	# HPA RNA cell lines
	cell_lines_hpa = pd.read_csv('./data/HPA/rna_celline.tsv', sep = '\t')
	cell_info_hpa = [str(c).upper().replace('-', '') for c in cell_lines_hpa['Sample'].unique()]
	breast_cancer_cell_lines_hpa = [c for c in cell_info_hpa if c in b.breast_cancer_information['Cell lines'].tolist()]

	# HPA tissue
	tissue_rna_hpa = pd.read_csv('./data/HPA/rna_tissue.tsv', sep = '\t')
	breast_tissue_rna_hpa = tissue_rna_hpa[tissue_rna_hpa['Sample']=='breast'].drop(columns='Sample')

	# HPA transcript RNA Cell Line
	trans_rna_hpa_cell_line = pd.read_csv('./data/HPA/transcript_rna_celline.tsv', sep = '\t')
	trans_rna_hpa_cell_line_names = [str(c).upper().replace('-', '').split('.')[0] for c in trans_rna_hpa_cell_line.columns]
	trans_rna_hpa_cell_line_breast = [c for c in trans_rna_hpa_cell_line_names if c in b.breast_cancer_information['Cell lines'].tolist()]