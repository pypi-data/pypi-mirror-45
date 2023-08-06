NAME = 'name'
DOCUMENTATION = 'documentation'
METRIC_OBJECT = 'metric_object'
COUNTERS = 'counters'
SHOW_MODEL = 'show_model'
GET_MODEL = 'get_model'
GAUGES = 'gauges'
BUILD_DURATION = 'build_duration'
ACCURACY = 'accuracy'
ERROR_RATE = 'error_rate'
TRAIN_SET_SIZE = 'train_set_size'
TEST_SET_SIZE = 'test_set_size'
DATASET_SIZE = 'dataset_size'

metrics_dict = {
    COUNTERS: {
        SHOW_MODEL: {
            NAME: SHOW_MODEL,
            DOCUMENTATION: 'show model request counter',
            METRIC_OBJECT: None
        },
        GET_MODEL: {
            NAME: GET_MODEL,
            DOCUMENTATION: 'get model request counter',
            METRIC_OBJECT: None
        }
    },
    GAUGES: {
        BUILD_DURATION: {
            NAME: BUILD_DURATION,
            DOCUMENTATION: 'model duration time metric',
            METRIC_OBJECT: None
        },
        ACCURACY: {
            NAME: ACCURACY,
            DOCUMENTATION: 'model accuracy metric',
            METRIC_OBJECT: None
        },
        ERROR_RATE: {
            NAME: ERROR_RATE,
            DOCUMENTATION: 'model error rate metric',
            METRIC_OBJECT: None
        },
        TRAIN_SET_SIZE: {
            NAME: TRAIN_SET_SIZE,
            DOCUMENTATION: 'model train set size metric',
            METRIC_OBJECT: None
        },
        TEST_SET_SIZE: {
            NAME: TEST_SET_SIZE,
            DOCUMENTATION: 'model test set size metric',
            METRIC_OBJECT: None
        },
        DATASET_SIZE: {
            NAME: DATASET_SIZE,
            DOCUMENTATION: 'model dataset size metric',
            METRIC_OBJECT: None
        }
    }
}
