// t/test.cpp
#include "CppUTest/TestHarness.h"
#include "include.h"

#ifdef __cplusplus
extern "C" {
#endif
//DATA STRUCTURES
typedef enum{
    CSE = 0, EEE, EGR, SER
} Subject;

typedef struct CourseNode{
    Subject subject;
    int number;
    char teacher[1024];
    int credit_hours;
    struct CourseNode* next;
} CourseNode;

//FORWARD DECLARATIONS
extern void branching(char option);
extern int getCreditCount();
extern void course_insert(Subject subject, int number, char teacher[1024], int credit_hours);
extern int duplicate_class(Subject subject, int number, char teacher[1024], int credit_hours);
extern void schedule_print();
extern void course_drop(Subject subject, int number);
extern void schedule_load();
extern void schedule_save();
extern int file_exists(char string[]);

//GLOBAL VARIABLES
extern CourseNode* course_collection;

#ifdef __cplusplus
}
#endif

TEST_GROUP(tests)
{
};

TEST(tests, CreditCountTest)
{
  course_collection = (CourseNode*) malloc(sizeof(CourseNode));
  CourseNode* node = course_collection;
  node->credit_hours = 1;
  node->next = NULL;

  CHECK_EQUAL(1, getCreditCount()); //case 1


  node->next = (CourseNode*) malloc(sizeof(CourseNode));
  node = node->next;
  node->credit_hours = 3;
  node->next = NULL;

  CHECK_EQUAL(4, getCreditCount()); //case 2


  node->next = (CourseNode*) malloc(sizeof(CourseNode));
  node = node->next;
  node->credit_hours = 2;
  node->next = NULL;

  CHECK_EQUAL(6, getCreditCount()); //case 3

  node = course_collection;
  while (node != NULL) {
    CourseNode *tmp = node;
    node = node->next;
    free(tmp);
  }
  course_collection = NULL;

  CHECK_EQUAL(0, getCreditCount()); //case 4
}

TEST(tests, DuplicateClassTest)
{
  
  CHECK_EQUAL(0, duplicate_class(SER, 333, "foo", 3)); //case 1

  course_collection = (CourseNode*) malloc(sizeof(CourseNode));
  CourseNode* node = course_collection;
  node->number = 333;
  node->subject = SER;
  node->next = NULL;

  CHECK_EQUAL(1, duplicate_class(SER, 333, "foo", 3)); //case 2
  CHECK_EQUAL(0, duplicate_class(SER, 332, "foo", 3)); //case 3
  CHECK_EQUAL(0, duplicate_class(CSE, 333, "foo", 3)); //case 4

  node->next = (CourseNode*) malloc(sizeof(CourseNode));
  node = node->next;
  node->number = 240;
  node->subject = CSE;
  node->next = NULL;

  node->next = (CourseNode*) malloc(sizeof(CourseNode));
  node = node->next;
  node->number = 101;
  node->subject = EGR;
  node->next = NULL;

  CHECK_EQUAL(1, duplicate_class(SER, 333, "foo", 3)); //case 5
  CHECK_EQUAL(1, duplicate_class(EGR, 101, "foo", 3)); //case 6
  CHECK_EQUAL(1, duplicate_class(CSE, 240, "foo", 3)); //case 7

  node = course_collection;
  while (node != NULL) {
    CourseNode *tmp = node;
    node = node->next;
    free(tmp);
  }
  course_collection = NULL;
}
