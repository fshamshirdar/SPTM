MIN_SHORTCUT_DISTANCE = 5
SHORTCUT_WINDOW = 10
GOAL_SIMILARITY_THRESHOLD = 0.8
SHORTCUT_SIMILARITY_THRESHOLD = 0.8
ACTION_LOOKAHEAD_PROB_THRESHOLD = 0.8
ACTION_LOOKAHEAD_ENABLED = True
SEQUENCE_VELOCITIES = [0.0, 0.3, 0.5, 0.8, 1.0, 1.5]
SEQUENCE_LENGTH = 5

AIRSIM_MODE_DATA_COLLECTION = 1
AIRSIM_MODE_TEACH = 2
AIRSIM_MODE_REPEAT = 3
AIRSIM_MODE_REPEAT_BACKWARDS = 4

BEBOP_MODE_IDLE = 0
BEBOP_MODE_TEACH_MANUALLY = 1
BEBOP_MODE_TEACH = 2
BEBOP_MODE_REPEAT = 3

BEBOP_MODE_STRINGS = { BEBOP_MODE_IDLE: "IDLE", BEBOP_MODE_TEACH_MANUALLY: "TEACH_MANUALLY",
                       BEBOP_MODE_TEACH: "TEACH", BEBOP_MODE_REPEAT: "REPEAT" }

LOCO_IMAGE_SIZE = 224
LOCO_IMAGE_WIDTH = 224
LOCO_IMAGE_HEIGHT = 224
LOCO_NUM_CLASSES = 3

PLACE_NETWORK_RESNET18 = 1
PLACE_NETWORK_PLACENET = 2
PLACE_NETWORK = PLACE_NETWORK_PLACENET
PLACE_IMAGE_SIZE = 227
PLACE_IMAGE_WIDTH = 227
PLACE_IMAGE_HEIGHT = 227
PLACE_NUM_CLASSES = 3

TRAINING_LOCO_IMAGE_SCALE = 224
TRAINING_LOCO_BATCH = 32
TRAINING_LOCO_LR = 0.01
TRAINING_LOCO_MOMENTUM = 0.9
TRAINING_LOCO_LR_SCHEDULER_SIZE = 7
TRAINING_LOCO_LR_SCHEDULER_GAMMA = 0.1

TRAINING_PLACE_IMAGE_SCALE = 227
TRAINING_PLACE_BATCH = 32
TRAINING_PLACE_MARGIN = 0.5 # 300 # 0.2
TRAINING_PLACE_LR = 0.01 # 0.0005 # 0.01
TRAINING_PLACE_MOMENTUM = 0.9
TRAINING_PLACE_LR_SCHEDULER_SIZE = 7
TRAINING_PLACE_LR_SCHEDULER_GAMMA = 0.1
TRAINING_PLACE_NEGATIVE_SAMPLE_MIN_INDEX = 5
TRAINING_PLACE_NEGATIVE_SAMPLE_MAX_INDEX = 20

DATA_COLLECTION_ROUNDS = 2000
DATA_COLLECTION_MIN_ANGLE = 0.174533 # 10 deg
DATA_COLLECTION_MAX_ANGLE = 0.92173 # 52 deg
DATA_COLLECTION_MIN_SPEED = 0.5
DATA_COLLECTION_MAX_SPEED = 3.0
DATA_COLLECTION_PLAYING_ROUNG_LENGTH = 100
DATA_COLLECTION_MIN_HEIGHT = 1
DATA_COLLECTION_MAX_HEIGHT = 20

BEBOP_STRAIGHT_SPEED = 0.1
BEBOP_YAW_SPEED = 0.1
BEBOP_ACTION_DURATION = 1.0
BEBOP_ACTION_FREQ = 0.1
BEBOP_ACTION_STOP_DURATION = 0.5
BEBOP_TEACH_STOP_DURATION = 0.3

DATASET_MAX_ACTION_DISTANCE = 1

AIRSIM_AGENT_TEACH_LEN = 10

JOY_BUTTONS_TEACH_ID = 0
JOY_BUTTONS_LAND_ID = 1
JOY_BUTTONS_REPEAT_ID = 2
JOY_BUTTONS_TAKEOFF_ID = 3
JOY_BUTTONS_IDLE_ID = 4
JOY_BUTTONS_MANUAL_CONTROL_ID = 5
JOY_BUTTONS_CLEAR_MEMORY_ID = 6
