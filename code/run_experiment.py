from experiments.Segmentator import Segmentator
from experiments.Experiment import Experiment
from experiments.Model import Model
import threading
import os
import shutil

#***************************************************************************************************************
if __name__ == "__main__":
	# ************************************************************************************************
	# 						Base parameters for the set of experiments to be conducted
	# ************************************************************************************************
	def get_base_parameters(base_project_path, experiment_name, model_template):
		NN_code_directory 				= os.path.join(base_project_path, "code/CNN")
		dataset_directory				= os.path.join(base_project_path, "datasets")
		experimental_results_directory  = os.path.join(base_project_path, "experimental_results")

		model_name 						= model_template.replace("_template", "")
		base_training_parameters = {
			"GPU_identifier"	: 2,
			"number_of_GPUs"	: 4,
			"savingDirectory"	: os.path.join(experimental_results_directory, experiment_name),
			"presavedModelPath"	: "",
			"modelFilePath"		: os.path.join(os.path.join(NN_code_directory, "models"), model_name),
			"maxepoch"			: 100, 
			"learningRate"		: 0.01, 
			"batchSize"			: 1500*4, 
			"momentum"			: 0, 
			"training_dataset" 	: os.path.join(dataset_directory,"no_atrium_box_training_dataset.hdf5"),
			"testing_dataset" 	: os.path.join(dataset_directory,"testing_dataset.hdf5")
		}

		base_model_parameters = {
			"NN_code_directory"		: NN_code_directory,
			"modelTemplateDirectory": os.path.join(NN_code_directory, "model_templates"),
			"modelTemplate" 		: model_template,
			"modelFilePath"			: os.path.join(os.path.join(NN_code_directory, "models"), model_name),
			"activation_function"	: "ReLU",
			"pooling_function"		: "SpatialMaxPooling",
			"nfeaturemaps"  		: [32,64,1000,500],
			"filtsize" 	  			: 5,
			"poolsize" 	  			: [2,2],
			"featuremaps_h" 		: 5,
			"featuremaps_w" 		: 5,
			"noutputs" 	  			: 2
		}

		return dict(base_training_parameters), dict(base_model_parameters)

	def start_experiment(training_parameters, model_parameters):
		# Train the model
		model 		= Model(training_parameters, model_parameters)
		experiment 	= Experiment(model)
		experiment.run_experiment()

	# ************************************************************************************************
	# 										Run the experiments for varying parameters
	# ************************************************************************************************
	base_project_path 	= os.path.abspath("..")
	dataset_directory	= os.path.join(base_project_path, "datasets")

	experiment_name 	= "varying_number_of_convolutional_layers/1_conv_layer"
	model_template 		= "model_template_1_conv_layers.lua"
	training_parameters, model_parameters = get_base_parameters(base_project_path, experiment_name, model_template)
	model_parameters["nfeaturemaps"]  	= [32,1000,500]
	model_parameters["featuremaps_h"] 	= 14
	model_parameters["featuremaps_w" ]	= 14

	start_experiment(training_parameters, model_parameters)

	experiment_name 	= "varying_number_of_convolutional_layers/2_conv_layers"
	model_template 		= "model_template_2_conv_layers.lua"
	training_parameters, model_parameters = get_base_parameters(base_project_path, experiment_name, model_template)
	model_parameters["nfeaturemaps"]  	= [32,64,1000,500]
	model_parameters["featuremaps_h"] 	= 5
	model_parameters["featuremaps_w" ]	= 5

	start_experiment(training_parameters, model_parameters)

	experiment_name 	= "varying_number_of_convolutional_layers/3_conv_layers"
	model_template 		= "model_template_3_conv_layers.lua"
	training_parameters, model_parameters = get_base_parameters(base_project_path, experiment_name, model_template)
	model_parameters["nfeaturemaps"]  	= [32,32,64,1000,500]
	model_parameters["featuremaps_h"] 	= 4
	model_parameters["featuremaps_w" ]	= 4

	start_experiment(training_parameters, model_parameters)

	experiment_name 	= "varying_number_of_convolutional_layers/4_conv_layers"
	model_template 		= "model_template_4_conv_layers.lua"
	training_parameters, model_parameters = get_base_parameters(base_project_path, experiment_name, model_template)
	model_parameters["nfeaturemaps"]  	= [32,32,64,64,1000,500]
	model_parameters["featuremaps_h"] 	= 2
	model_parameters["featuremaps_w" ]	= 2

	start_experiment(training_parameters, model_parameters)



