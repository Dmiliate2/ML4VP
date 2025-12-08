clc; clear all

% --- Paths ---
model_dirpath = "./GPR_10_Ensemble";
results_dirpath = "../New_Molecules";
filename = "Features.csv";
output_filename = "GPR_Predictions.csv";
new_molecules_filepath = fullfile(results_dirpath, filename); 

% --- Load models ---
model_files = dir(fullfile(model_dirpath, "*.mat"));
numModels = numel(model_files);
listOfModels = cell(numModels,1);
subsetIDs = strings(numModels,1);
for i = 1:numModels
    filepath = fullfile(model_dirpath, model_files(i).name);
    fprintf("Loading model: %s\n", model_files(i).name);
    listOfModels{i} = loadLearnerForCoder(filepath);

    % --- Extract Subset ID from filename (pattern: SubsetIndex_#####)
    token = regexp(model_files(i).name, 'SubsetIndex_(\d+)', 'tokens');
    if ~isempty(token)
        subsetIDs(i) = token{1}{1};
    else
        subsetIDs(i) = "Unknown";
    end
end

% --- Determine relevant features from all models ---
allFeatureNames = {};
for i = 1:numModels
    fnames = listOfModels{i}.PredictorNames;  % for exported models
    allFeatureNames = [allFeatureNames, fnames];
end
allFeatureNames = [allFeatureNames, "SMILES"];
uniqueFeatures = unique(allFeatureNames);

% --- Read input data ---
T = readtable(new_molecules_filepath, VariableNamingRule="preserve");

% --- Predict with each model ---
numObs = height(T);
Y_all = nan(numObs, numModels);
for i = 1:numModels
    mdl = listOfModels{i};
    fprintf("Predicting with model %d...\n", i);

    try
        y_pred = predict(mdl, T);
    catch
        warning("Model %d prediction failed. Filling with NaNs.", i);
        y_pred = nan(numObs,1);
    end

    Y_all(:,i) = y_pred;
end

% --- Compute ensemble mean and std across models ---
Prediction_Mean = mean(Y_all, 2, 'omitnan');
Prediction_Std  = std(Y_all, 0, 2, 'omitnan');

% --- Build result table with each model's predictions ---
results_table = table();
for i = 1:numModels
    varName = sprintf("Pred_%s", subsetIDs(i));
    results_table.(varName) = Y_all(:,i);
end

% --- Combine all results ---
final_table = [T, results_table, table(Prediction_Mean, Prediction_Std)];

% --- Write results ---
output_filepath = fullfile(results_dirpath, output_filename);
writetable(final_table, output_filepath);


fprintf("Predictions saved to: %s\n", output_filepath);

