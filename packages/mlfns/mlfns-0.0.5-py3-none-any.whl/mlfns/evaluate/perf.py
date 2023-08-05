import numpy as np
import pandas as pd
from sklearn import metrics

##############################################################################
# EVALUATION - Model performance
#
#  TODO: ROC (see tl_techniques.ipynb
##############################################################################
def summarize_evaluation(metrics, model=None):
    """
    Summary of model evaluation metrics from Keras "evaluate" method;
    the evaluation is typically performed for test dataset.
    Metrics include: loss and accuracy 
    
    # Arguments
        metrics: metrics return by the Keras evaluate() method
        model: the model evaluated;
            if provided the attribute "metrics_names" will be used to
            obtain the metric names                  
                  
    # Returns
        None
    
    # Raise
        None
    """
    print('\nSummary - Model Evaluation:')
    print('-'*30)
    if model:
        no_metrics = len(model.metrics_names)
        for i in range(no_metrics):
            print('  {} = {:.3f}'.format(model.metrics_names[i], metrics[i]))
    else:
        loss = metrics[0]
        acc = (metrics[1]*100)
        print('  (Loss, Accuracy) = ({:.3f}, {:.3f}%)'.format(loss, acc))


def model_perf_summary(actual_labels, predicted_labels, classes=[1,0]):
    """
    Summarize model performance metrics: Accuracy, Precision, Recall, and
    F1 score.
    
    # Arguments
        actual_labels: the actual label provided with the dataset;
            type=<list>; shape = (n); n=total no. of labels
        predicted_labels: labels predicted by the model;
            type, shape = same as actual_labels
        classes: list of classes used by the labels;
            type=<list>; shape = (m); m=total number of classes
            for binary classification, the "classes" has two entries

    # Returns
        None
    
    # Raise
        None
    """
    print('\nModel Performance metrics:')
    print('-'*30)
    print('Number of data: {}'.format(len(actual_labels)))
    print('Accuracy:', np.round(metrics.accuracy_score(actual_labels, 
                                  predicted_labels), 4))
    print('Precision:', np.round(metrics.precision_score(actual_labels,
                                    predicted_labels, average='weighted'), 4))
    print('Recall:', np.round(metrics.recall_score(actual_labels,
                                    predicted_labels, average='weighted'), 4))
    print('F1 Score:', np.round(metrics.f1_score(actual_labels, 
                                    predicted_labels, average='weighted'), 4))


def classification_rpt(actual_labels, predicted_labels, classes=[1,0]):
    """
    Classification report summarizes model performance metrics
    (i.e., Accuracy, Precision, Recall, and F1 score), and grouped by
    classes; as well as the micro, macro and weighted average.
    
    # Arguments
        actual_labels: the actual label provided with the dataset;
            type=<list>; shape = (n); n=total no. of labels
        predicted_labels: labels predicted by the model;
            type, shape = same as actual_labels
        classes: list of classes used by the labels;
            type=<list>; shape = (m); m=total number of classes
            for binary classification, the "classes" has two entries

    # Returns
        None
    
    # Raise
        None
    """
    print('\nModel Classification report:')
    print('-'*30)
    report = metrics.classification_report(y_true=actual_labels, 
                                           y_pred=predicted_labels, 
                                           labels=classes) 
    print(report)


def confusion_matrix(actual_labels, predicted_labels, classes=[1,0]):
    """
    Confusion matrix.
    
    # Arguments
        actual_labels: the actual label provided with the dataset;
            type=<list>; shape = (n); n=total no. of labels
        predicted_labels: labels predicted by the model;
            type, shape = same as actual_labels
        classes: list of classes used by the labels;
            type=<list>; shape = (m); m=total number of classes
            for binary classification, the "classes" has two entries

    # Returns
        None
    
    # Raise
        None        
    """
    print('\nPrediction Confusion Matrix:')
    print('-'*30)
    total_classes = len(classes)
    level_labels = [total_classes*[0], list(range(total_classes))]
    cm = metrics.confusion_matrix(y_true=actual_labels, y_pred=predicted_labels,
                                    labels=classes)
    cm_frame = pd.DataFrame(data=cm, 
                            columns=pd.MultiIndex(levels=[['Predicted:'],
                                                  classes],
                                                  labels=level_labels), 
                            index=pd.MultiIndex(levels=[['Actual:'], classes], 
                                                labels=level_labels)) 
    print(cm_frame)

