MIN_SHORTCUT_DISTANCE = 5
SHORTCUT_WINDOW = 10
GOAL_SIMILARITY_THRESHOLD = 0.8
SHORTCUT_SIMILARITY_THRESHOLD = 0.8
TRAIL_SIMILARITY_THRESHOLD = 0.7
ACTION_LOOKAHEAD_PROB_THRESHOLD = 0.8
ACTION_LOOKAHEAD_ENABLED = False
SEQUENCE_VELOCITIES = [0.0, 0.3, 0.5, 0.8, 1.0, 1.5]
SEQUENCE_LENGTH = 5

AIRSIM_MODE_DATA_COLLECTION = 1
AIRSIM_MODE_TEACH = 2
AIRSIM_MODE_REPEAT = 3
AIRSIM_MODE_REPEAT_BACKWARDS = 4

ROBOT_MODE_IDLE = 0
ROBOT_MODE_TEACH_MANUALLY = 1
ROBOT_MODE_TEACH = 2
ROBOT_MODE_REPEAT = 3

ROBOT_MODE_STRINGS = { ROBOT_MODE_IDLE: "IDLE", ROBOT_MODE_TEACH_MANUALLY: "TEACH_MANUALLY",
                       ROBOT_MODE_TEACH: "TEACH", ROBOT_MODE_REPEAT: "REPEAT" }

LOCO_IMAGE_SIZE = 224
LOCO_IMAGE_WIDTH = 224
LOCO_IMAGE_HEIGHT = 224
LOCO_NUM_CLASSES = 6

PLACE_NETWORK_RESNET18 = 1
PLACE_NETWORK_PLACENET = 2
PLACE_NETWORK = PLACE_NETWORK_RESNET18
PLACE_TOP_TRIPLET = 0
PLACE_TOP_SIAMESE = 1
PLACE_TOP_MODEL = PLACE_TOP_TRIPLET
PLACE_RESNET18_IMAGE_SIZE = 224
PLACE_RESNET18_IMAGE_WIDTH = 224
PLACE_RESNET18_IMAGE_HEIGHT = 224
PLACE_PLACENET_IMAGE_SIZE = 227
PLACE_PLACENET_IMAGE_WIDTH = 227
PLACE_PLACENET_IMAGE_HEIGHT = 227
PLACE_IMAGE_SIZE = PLACE_RESNET18_IMAGE_SIZE if PLACE_NETWORK == PLACE_NETWORK_RESNET18 else PLACE_PLACENET_IMAGE_SIZE
PLACE_IMAGE_WIDTH = PLACE_RESNET18_IMAGE_WIDTH if PLACE_NETWORK == PLACE_NETWORK_RESNET18 else PLACE_PLACENET_IMAGE_WIDTH
PLACE_IMAGE_HEIGHT = PLACE_RESNET18_IMAGE_HEIGHT if PLACE_NETWORK == PLACE_NETWORK_RESNET18 else PLACE_PLACENET_IMAGE_HEIGHT

TRAINING_LOCO_IMAGE_SCALE = 224
TRAINING_LOCO_BATCH = 64
TRAINING_LOCO_LR = 0.001
TRAINING_LOCO_MOMENTUM = 0.9
TRAINING_LOCO_LR_SCHEDULER_SIZE = 5000
TRAINING_LOCO_LR_SCHEDULER_GAMMA = 0.1

TRAINING_PLACE_IMAGE_SCALE = 227
TRAINING_PLACE_BATCH = 32
TRAINING_PLACE_MARGIN = 0.8 # 300 # 0.2
TRAINING_PLACE_LR = 0.001 # 0.0005 # 0.01
TRAINING_PLACE_MOMENTUM = 0.9
TRAINING_PLACE_LR_SCHEDULER_SIZE = 5000
TRAINING_PLACE_LR_SCHEDULER_GAMMA = 0.1
TRAINING_PLACE_NEGATIVE_SAMPLE_MULTIPLIER = 5

DQN_LOCO_TEACH_LEN = 10
DQN_LOCO_TEACH_NUM_CONSISTENT_ACTION = 3
DQN_LOCO_REPEAT_LEN = 10
DQN_MEMORY_SIZE = 50000
DQN_REWARD_DISTANCE_OFFSET = 1.
DQN_REWARD_ANGLE_OFFSET = 0.
DQN_MAX_DISTANCE_THRESHOLD = 5.
DQN_LEARNING_OFFSET_START = 1000
DQN_LEARNING_FREQ = 1
DQN_LEARNING_RATE = 0.001
DQN_TARGET_UPDATE_FREQ = 1000
DQN_CHECKPOINT_FREQ = 1000
DQN_GAMMA = 0.99
DQN_BATCH_SIZE = 32
DQN_DISTANCE_REWARD_WEIGHT = 1.
DQN_ANGLE_REWARD_WEIGHT = 1.

DATA_COLLECTION_ROUNDS = 2000
DATA_COLLECTION_MIN_ANGLE = 0.174533 # 10 deg
DATA_COLLECTION_MAX_ANGLE = 0.92173 # 52 deg
DATA_COLLECTION_MIN_SPEED = 0.5
DATA_COLLECTION_MAX_SPEED = 3.0
DATA_COLLECTION_PLAYING_ROUNG_LENGTH = 1000
DATA_COLLECTION_ONLINE_TRAINING_ROUNG_LENGTH = 20000
DATA_COLLECTION_ONLINE_VALIDATING_ROUNG_LENGTH = 1000
DATA_COLLECTION_MIN_HEIGHT = 1
DATA_COLLECTION_MAX_HEIGHT = 20

AIRSIM_STRAIGHT_SPEED = DATA_COLLECTION_MIN_SPEED
AIRSIM_SIDE_SPEED = DATA_COLLECTION_MIN_SPEED
AIRSIM_YAW_SPEED = DATA_COLLECTION_MIN_ANGLE  # (DATA_COLLECTION_MIN_ANGLE + DATA_COLLECTION_MAX_ANGLE) / 2.

ACTION_MOVE_FORWARD = 0
ACTION_TURN_RIGHT = 1
ACTION_TURN_LEFT = 2
ACTION_MOVE_BACKWARD = 3
ACTION_MOVE_RIGHT = 4
ACTION_MOVE_LEFT = 5

VIZDOOM_DEFAULT_WAD = 'vizdoom/Train/D3_battle_navigation_split.wad_manymaps_test.wad'
VIZDOOM_DEFAULT_CONFIG = 'vizdoom/default.cfg'
VIZDOOM_MIN_RANDOM_TEXTURE_MAP_INDEX = 2
VIZDOOM_MAX_RANDOM_TEXTURE_MAP_INDEX = 401
VIZDOOM_MIN_TEST_MAP_INDEX = 2
VIZDOOM_MAX_TEST_MAP_INDEX = 5
VIZDOOM_MAP_NAME_TEMPLATE = 'map%02d'
VIZDOOM_MOVE_FORWARD = [0, 0, 0, 1, 0, 0, 0]
VIZDOOM_MOVE_BACKWARD = [0, 0, 0, 0, 1, 0, 0]
VIZDOOM_MOVE_LEFT = [1, 0, 0, 0, 0, 0, 0]
VIZDOOM_MOVE_RIGHT = [0, 1, 0, 0, 0, 0, 0]
VIZDOOM_TURN_LEFT = [0, 0, 0, 0, 0, 1, 0]
VIZDOOM_TURN_RIGHT = [0, 0, 0, 0, 0, 0, 1]
VIZDOOM_STAY_IDLE = [0, 0, 0, 0, 0, 0, 0] 
# VIZDOOM_ACTIONS_LIST = [VIZDOOM_MOVE_FORWARD, VIZDOOM_TURN_RIGHT, VIZDOOM_TURN_LEFT, VIZDOOM_MOVE_RIGHT, VIZDOOM_MOVE_LEFT, VIZDOOM_MOVE_BACKWARD]
VIZDOOM_ACTIONS_LIST = [VIZDOOM_MOVE_FORWARD, VIZDOOM_TURN_RIGHT, VIZDOOM_TURN_LEFT, VIZDOOM_MOVE_BACKWARD, VIZDOOM_MOVE_RIGHT, VIZDOOM_MOVE_LEFT]
VIZDOOM_GOAL_DISTANCE_THRESHOLD = 65

MULTI_NUM_AGENTS = 1
MULTI_AGENT_RANDOM_MOVEMENT_CHANCE = 0.2
MULTI_AGENT_STATE_SEARCH = 0
MULTI_AGENT_STATE_HOME = 1

TRAIL_EVAPORATION_COEFFICIENT_RATE = 0.003
TRAIL_STEP_TO_TARGET_WEIGHT = 7.0
TRAIL_SIMILARITY_WEIGHT = 3.0

BEBOP_STRAIGHT_SPEED = 0.1
BEBOP_YAW_SPEED = 0.1
BEBOP_ACTION_DURATION = 1.0
BEBOP_ACTION_FREQ = 0.1
BEBOP_ACTION_STOP_DURATION = 0.5
BEBOP_TEACH_STOP_DURATION = 0.3

PIONEER_STRAIGHT_SPEED = 0.1
PIONEER_YAW_SPEED = 0.1
PIONEER_ACTION_DURATION = 1.0
PIONEER_ACTION_FREQ = 0.1
PIONEER_ACTION_STOP_DURATION = 0.5
PIONEER_TEACH_STOP_DURATION = 0.3

DATASET_MAX_ACTION_DISTANCE = 5

AIRSIM_AGENT_TEACH_LEN = 10

JOY_BUTTONS_TEACH_ID = 0
JOY_BUTTONS_LAND_ID = 1
JOY_BUTTONS_REPEAT_ID = 2
JOY_BUTTONS_TAKEOFF_ID = 3
JOY_BUTTONS_IDLE_ID = 4
JOY_BUTTONS_MANUAL_CONTROL_ID = 5
JOY_BUTTONS_CLEAR_MEMORY_ID = 6
