import lib.dataset_functions as df
import os
import re
import math
import numpy as np
import h5py
import argparse

if __name__ == "__main__":
	# Setting Parameters
	parameters = {
		"data_directory" 		: "../../ct_atrium",
		"CT_scan_path_template" : "../../ct_atrium/CTScan_name",
		"NRRD_path_template"    : "../../ct_atrium/CTScan_name/CTScan_name.nrrd",
		"DICOM_path_template"   : "../../ct_atrium/CTScan_name/DICOMS/DICOM_name",
		"ct_directory_pattern"  : re.compile("[0-9]{8}"),
		"patch_size"    		: 32,
		"n_training_CT_scans"   : 22,
		"n_testing_CT_scans"	: 5,
		"n_training_examples_per_CT_scan" : 10000,
		"n_testing_examples_per_CT_scan"  : 20000,
		"pourcentage_atrium"	: 0.2
	}

	random  == True
	segment == False
	boxed   == True

	# ********************************************************************************************
	# 					Separate the CT scans into a training and testing set
	# ********************************************************************************************
	# Get the names of all the CT scans
	CT_scans = [directory for directory in os.listdir(data_directory) if CT_directory_pattern.match(directory)]

	CT_scan_dictionary = df.get_all_DICOMs(parameters["CT_scan_path_template"], CT_scans)

	np.random.seed(12)
	training_CT_scans = np.random.choice(CT_scans, parameters["n_training_CT_scans"], replace=False)
	testing_CT_scans  = [CT_scan for CT_scan in CT_scans if CT_scan not in training_CT_scans]

	# ********************************************************************************************
	# 						Generate the training and testing datasets
	# ********************************************************************************************
	if random == True:
		print "=======> Generating the training dataset <======="
		training_dataset, training_labels = df.generate_random_dataset(training_CT_scans, CT_scan_dictionary, parameters["n_training_examples_per_CT_scan"], parameters)
		print "=======> Generating the testing dataset <======="
		testing_dataset, testing_labels  = df.generate_random_dataset(testing_CT_scans, CT_scan_dictionary, parameters["n_testing_examples_per_CT_scan"], parameters)

		dataset_directory = os.path.join(parameters["data_directory"], "datasets")
		dataset_path      = os.path.join(dataset_directory, "CNN_datasets.hdf5")

		print "=======> Saving the training and testing datasets in %s <=======" %dataset_path
		f 			  		  	  = h5py.File(dataset_path, "w")
		# For the training dataset
		training_dataset_hdf5 	  	  = f.create_dataset("training_dataset", training_dataset.shape, dtype="uint32")
		training_dataset_hdf5[...]    = np.int16(training_dataset)
		training_labels_hdf5 	  	  = f.create_dataset("training_labels", training_labels.shape, dtype="uint8")
		training_labels_hdf5[...]  	  = np.int16(training_labels)
		# For the testing dataset
		testing_dataset_hdf5 	  	  = f.create_dataset("testing_dataset", testing_dataset.shape, dtype="uint32")
		testing_dataset_hdf5[...]  	  = np.int16(testing_dataset)
		testing_labels_hdf5 	  	  = f.create_dataset("testing_labels", testing_labels.shape, dtype="uint8")
		testing_labels_hdf5[...]  	  = testing_labels
		f.close()

	# ********************************************************************************************
	# 	  Generating the segmentation dataset from a dicom file of one of the testing CT scans
	# ********************************************************************************************
	if segment == True:
		segmented_CT_scan 		 = testing_CT_scans[0]
		segmented_CT_scan_DICOMS = df.get_DICOMs(parameters["CT_scan_path_template"].replace("CTScan_name", segmented_CT_scan))
		nrrd_path 		  		 = parameters["NRRD_path_template"].replace("CTScan_name", segmented_CT_scan)

		CT_scan_labels, CT_scan_nrrd_header 	 = df.get_NRRD_array(nrrd_path)
		CT_scan_3d_image  						 = df.get_CT_scan_array(segmented_CT_scan, segmented_CT_scan_DICOMS, 
																		CT_scan_nrrd_header["sizes"], parameters["DICOM_path_template"])
		dicom_height, dicom_width, number_dicoms = CT_scan_3d_image.shape
		x_grid, y_grid = range(dicom_height), range(dicom_width)

		tri_planar_segmentation_dataset = np.zeros((CT_scan_3d_image[:,:,0].size, 6, parameters["patch_size"], parameters["patch_size"]))

		z = 30
		print "=======> Generating the segmentation dataset from the DICOM file %i from CT scan %s... <=======" %(z, segmented_CT_scan)
		for x in y_grid:
			for y in x_grid:
				tri_planar_segmentation_dataset[y + dicom_width*x, :, :, :] = df.generate_patches(x,y,z,CT_scan_3d_image,parameters["patch_size"])

		segmentation_dataset_path = os.path.join(dataset_directory, "segmentation_datasets.hdf5")
		print "=======> Saving the segmentation dataset in %s <=======" %segmentation_dataset_path
		f 			  		  	  = h5py.File(segmentation_dataset_path, "w")
		segmentation_dataset_name = "segmentation_dataset"
		segmentation_dataset  	  = f.create_dataset(segmentation_dataset_name, tri_planar_segmentation_dataset.shape, dtype="uint8")
		segmentation_dataset.attrs["CT_scan"] 	   = segmented_CT_scan
		segmentation_dataset.attrs["DICOM_number"] = z
		segmentation_dataset[...] = tri_planar_segmentation_dataset
		segmentation_label_name   = "segmentation_labels"
		segmentation_label  	  = f.create_dataset(segmentation_label_name, CT_scan_labels[:,:,z].shape, dtype="uint8")
		segmentation_label[...]   = CT_scan_labels[:,:,z]
		segmentation_values_name  = "segmentation_values"
		segmentation_values  	  = f.create_dataset(segmentation_values_name, CT_scan_3d_image[:,:,z].shape, dtype="uint8")
		segmentation_values[...]  = CT_scan_3d_image[:,:,z]








