# we don’t want to use relative paths, so we set these variables
PROJECT_DIR=/home/charles/C_Projects/SER334/honors_contract/git/my_shoggoth/C/SERXXX_AssignmentNum_Test_Project/
SRC_DIR=$(PROJECT_DIR)/src
TEST_DIR=$(PROJECT_DIR)/tests

# specify where the source code and includes are located
INCLUDE_DIRS=$(SRC_DIR)/code /home/charles/C_Projects/SER334/honors_contract/git/cpputest/include/
SRC_DIRS=$(SRC_DIR)/code

# specify where the test code is located
TEST_SRC_DIRS = $(TEST_DIR)

# what to call the test binary
TEST_TARGET=example

# where the cpputest library is located
CPPUTEST_HOME=/home/charles/C_Projects/SER334/honors_contract/git/cpputest
