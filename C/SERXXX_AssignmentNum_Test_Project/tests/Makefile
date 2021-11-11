# we don’t want to use relative paths, so we set these variables
PROJECT_DIR=/autograder/source/SERXXX_AssignmentNum_Test_Project
SRC_DIR=$(PROJECT_DIR)/src
TEST_DIR=$(PROJECT_DIR)/tests

# specify where the source code and includes are located
INCLUDE_DIRS=$(SRC_DIR)/code /autograder/cpputest/include
SRC_DIRS=$(SRC_DIR)/code

# specify where the test code is located
TEST_SRC_DIRS = $(TEST_DIR)

# what to call the test binary
TEST_TARGET=example

# where the cpputest library is located
CPPUTEST_HOME=/autograder/cpputest

#change directories for local environment (not docker container)
#comment this line out for deployment to gradescope
include localDirs.mk

#manually set warn flags so we don't end up with something idiotic like -Wall -Wextra -Werror (seriously how is that default???)
CPPUTEST_WARNINGFLAGS = -Wall -Wextra -Wshadow -Wswitch-default -Wswitch-enum -Wconversion -Wno-long-long

#generate coverage maps
#CPPUTEST_USE_GCOV=Y

#flags for test executable
CPPUTEST_EXE_FLAGS = -o junit

# run MakefileWorker.mk with the variables defined here
include MakefileWorker.mk