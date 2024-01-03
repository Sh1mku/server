import joblib
import numpy as np


# define the gloabl variables

Locomotion_activities = {0: "Unlabelled Activity", 1:"Stand", 2:"Walk", 4:"Sit", 5:"Lie"}

label_to_activity = {
  406516: 'Open Door 1',
  406517: 'Open Door 2',
  404516: 'Close Door 1',
  404517: 'Close Door 2',
  406520: 'Open Fridge',
  404520: 'Close Fridge',
  406505: 'Open Dishwasher',
  404505: 'Close Dishwasher',
  406519: 'Open Drawer 1',
  404519: 'Close Drawer 1',
  406511: 'Open Drawer 2',
  404511: 'Close Drawer 2',
  406508: 'Open Drawer 3',
  404508: 'Close Drawer 3',
  408512: 'Clean Table',
  407521: 'Drink from Cup',
  405506: 'Toggle Switch' }

anomalies = {406516: [4,5], 404516: [4,5], 406520:[5], 406505: [4,5], 404505: [4,5],
             406519: [4, 5], 404519: [4,5], 408512: [4,5], 407521: [5], 405506: [4,5]}


# Load the trained models
Locomotion_model = joblib.load('rf_locomotion.joblib')
Locomotion_scaler = joblib.load('rf_scaler_locomotion.joblib')

# Objects_model  =
# Objects_scalar =

def perform_inference_locomotion(new_data):
    # order of features should match the order used during training

    # Drop unnecessary columns (since we are using holdout test dataset right now, we have to do this)
    # and if we send all the data from the server and use the anomaly detector function instead,
    # we would still need to drop the unncessary columns
    cols_to_drop = [i for i in range(136, 232)]
    df = new_data.drop(new_data.columns[cols_to_drop], axis=1)


    # dropping these label columns for the test dataset, obviously they wont be there in real
    # sensors data received from server
    X = np.asarray(df.drop([1,244,245,246,247,248,249,250], axis=1))
    y = np.asarray(df[244])   # this is for testing purposes to see if correct label is being predicted
    y = y.astype('int')

    # Perform inference
    prediction_proba = Locomotion_model.predict_proba(Locomotion_scaler.transform(X))
    predicted_class = np.argmax(prediction_proba)
    predicted_probability = np.max(prediction_proba) * 100

    # check if correct label is being predicted: we can do this for the test set only:

    print("Actual label: ", y[0])
    print("Predicted label: ", predicted_class)
    print("Predicted probability: ", predicted_probability)
    print("--------------------------")

    # extract the class label
    predicted_activity = Locomotion_activities[predicted_class]

    # we need predicted_class for anomaly detector and predicted_activity/confidence for the frontend
    return predicted_class, predicted_activity, predicted_probability



def perform_inference_object(new_data):

    # # order of features should match the order used during training

    # # Drop unnecessary columns (since we are using holdout test dataset right now, we have to do this)
    # # and if we send all the data from the server and use the anomaly detector function instead,
    # # we would still need to drop the unncessary columns
    # cols_to_drop = [i for i in range(136, 232)]
    # df = new_data.drop(new_data.columns[cols_to_drop], axis=1)

    # X = np.asarray(df.drop([1,244,245,246,247,248,249,250], axis=1))
    # y = np.asarray(df[249])
    # y = y.astype('int')

    # # Perform inference
    # prediction_proba = Locomotion_model.predict_proba(Locomotion_scaler.transform(X))
    # predicted_class = np.argmax(prediction_proba)
    # predicted_probability = np.max(prediction_proba) * 100
    #
    # # check if correct label is being predicted: we can do this for the test set only:
    #
    # print("Actual label: ", y[0])
    # print("Predicted label: ", predicted_class)
    # print("Predicted probability: ", predicted_probability)
    # print("--------------------------")

    # we need predicted_class for anomaly detector and predicted_activity/confidence for the frontend
    # return predicted_class, predicted_activity, confidence_percentage
    pass


def anomaly_detector(new_data):

    # label1, object_activity, confidence_object = perform_inference_object(new_data)
    label2, locomotion_activity, confidence_locomotion = perform_inference_locomotion(new_data)

    # for now label1 being set to 406516
    label1 = 406516

    # just for sake of completeness but will be fixed once our model 2 is fixed
    object_activity = "unknown"
    confidence_object = 0

    if label2 in anomalies[label1]:
        return True, locomotion_activity, confidence_locomotion, object_activity, confidence_object
    else:
        return False, locomotion_activity, confidence_locomotion, object_activity, confidence_object