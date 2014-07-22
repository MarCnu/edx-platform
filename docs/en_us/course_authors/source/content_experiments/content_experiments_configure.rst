.. _Configure Your Course for Content Experiments:

#####################################################
Configure Your Course for Content Experiments
#####################################################

This chapter describes how to configure your course so that you can use content
experiments. See:

* :ref:`Enable Content Experiments`
* :ref:`Overview of Group Configurations`
* :ref:`Set up Group Configurations in edX Studio`
* :ref:`Guidelines for Modifying Group Configurations`
* :ref:`Set up Group Configurations in an XML Course`

.. _Enable Content Experiments:

****************************************
Enable Content Experiments
****************************************

To enable content experiments in your course, you add ``split_test`` to the
``advanced_modules`` policy key.

.. note::  
  ``split_test`` is the internal edX Platform name for a content experiment.

#. From the **Settings** menu, select **Advanced Settings**.
#. In the **Advanced Settings** page, find the ``advanced_modules`` policy key.
#. In the **Policy Value** field, add ``"split_test"``. 
   
   Be sure that you use the double quotation marks around the value, and that
   if you use multiple values for the key that they are separated by commas
   (``,``).

#. At the bottom of the page, click **Save Changes**.


.. _Overview of Group Configurations:

****************************************
Overview of Group Configurations
****************************************

Before you can create content experiments, you must specify group
configurations.

A group configuration defines how many groups of students are in an experiment.
You can have any number of group configurations in your course. When you create
a content experiment, you select the group configuration to use.

For example, you may want to do one content experiment that presents either a
video or a reading assignment to your students, and another content experiment
that presents the same question using four different problem types. For the
first content experiment, you need a group configuration that assigns your
students to two groups, and for the second content experiment, you need a
group configuration that assigns your students to four groups.

=============================
Assigning Students to Groups
=============================

The edX Platform assigns students to groups.

Group assignments are:

* Dynamic

  The edX Platform assigns a student to a group the first time he or she views
  a content experiment that uses the group configuration.

* Random
  
  You cannot control which students are assigned to which group. 
  
* Evenly distributed
  
  The edX Platform keeps track of the size of groups and assigns new students
  to groups evenly. For example, when there are two groups in a configuration,
  each group will include 50% of the students in the course; when you have four
  groups, each group will include 25%.

* Permanent
  
  Students remain in their assigned groups regardless of how many content
  experiments you set up that use the same group configuration.

.. _Set up Group Configurations in edX Studio:

************************************************
Set up Group Configurations in edX Studio 
************************************************

You must :ref:`enable content experiments<Enable Content Experiments>` before
you can set up group configurations.

To set up group configurations, from the **Advanced** menu, select **Group
Configurations**. The **Group Configurations** page opens:

.. image:: ../Images/group_configurations.png
 :alt: The Group Configurations page

From this page you can create, edit, and delete group configurations. You can also view experiments that use a group configuration.

=============================
Create a Group Configuration
=============================

#. In the **Group Configurations** page, click **New Group Configuration** or
   **Add your first Group Configuration**. The following page opens:

  .. image:: ../Images/create-group-config.png
   :alt: Create a New Group Configuration page

2. Enter a name in the **Group Configuration Name** field. Use a meaningful
   name, as you select from group configuration names when creating content
   experiments. Students will not see the name.

#. Optionally, enter a description for the new group configuration.
#. Modify groups in the configuration as needed:

  * Click **Add another group** to include another group as part of the
    configuration.
  * Click the **X** to the right of an existing group to remove it from the
    configuration. Note that the configuration must have at least two groups.
  * Modify the group names as needed. You see group names in the unit page in
    Studio; students do not see group names.

5. Click **Create** to save the new group configuration.
   
The group configuration is then listed in the page:

.. image:: ../Images/group_configurations_one_listed.png
 :alt: The Group Configurations page with one group configuration
   
=============================
Edit a Group Configuration
=============================

.. note:: 
  Before modifying groups within a group configuration that is currently used
  in a running course, review `Guidelines for Modifying Group
  Configurations`_.

#. In the **Group Configurations** page, hover over the group configuration and
   click **Edit**.
   
   .. image:: ../Images/group_configurations_edit.png
    :alt: The Group Configurations page with Edit button

   The following page opens:

   .. image:: ../Images/save-group-config.png
    :alt: Edit a Group Configuration page

#. Modify the name and description as needed.
#. Modify groups in the configuration as needed:

  * Click **Add another group** to include another group as part of the
    configuration.
  * Click the **X** to the right of an existing group to remove it from the
    configuration. Note that the configuration must have at least two groups.
  * Modify the group names as needed. You see group names in the unit page in
    Studio; students do not see group names.
   
4. Click **Save** to save your changes.

=============================
Delete a Group Configuration
=============================

.. warning:: 
 Do not delete a group configuration that is used in the courseware after your
 course has started.

STEPS TBP

===============================================
View Experiments that Use a Group Configuration
===============================================

When working with group configurations, you can view the experiments that use
each configuration.

In the Group Configuration page, expand a group to see its details. You see
links to experiments that use the group configuration:

.. image:: ../Images/group_configurations_experiments.png
 :alt: A Group Configuration with the experiments using it circled

.. _Guidelines for Modifying Group Configurations:

*********************************************
Guidelines for Modifying Group Configurations
*********************************************

Review these guidelines if you must modify a group configuration after a course
starts. These guidelines apply for courses built in Studio or XML.

==================================
Modifying a Group Configuration
==================================

After the course starts, **do not**:

* Delete group configurations.

* Change the ``id`` value of a group configuration.
  
You can add group configurations or change group configuration names at any
time.

=================
Modifying Groups
=================

After the course starts, **do not** change the ``id`` value of a group.
  
You can change group names at any time.

==========================================================
Removing Groups from Group Configurations
==========================================================

After a course has started, you may find that students in a specific group are
having difficulties or a poor experience. In this situation, you can remove the
group from the group configuration. Content that was specified for that
group is then no longer visible to students.

Students in the removed group are reassigned evenly to one of the other groups
in the group configuration. Any problems that these students completed in the
removed group content do not count toward the students' grades. The students
must begin the problem set again and complete all the problems in the group
content to which they've been reassigned.

Removing a group impacts the course event data. Ensure that researchers
evaluating your course results are aware of the group you removed and the
date you removed it.

.. _Set up Group Configurations in an XML Course:

************************************************
Set up Group Configurations in an XML Course 
************************************************

If you are developing your course in XML, you define group configurations in
the ``policy.json`` file in the ``policies`` directory.

See :ref:`Add a Content Experiment in XML` for more information on how the XML
for the content experiment uses these settings.

To specify group configurations, you modify the value for the
``user_partitions`` policy key.

.. note::  
  ``user_partitions`` is the internal edX Platform name for group
  configurations.

The value for ``user_partitions`` is a JSON collection of group configurations,
each of which defines the groups of students. 

.. note:: 
  Use names for group configurations that are meaningful. You select from the
  list of group configuration names when you add a content experiment.

See the following examples for more information.

=============================================
Example: One Group Configuration
=============================================

The following is an example JSON object that defines an group configuration
with two student segments.

.. code-block:: json

    "user_partitions": [{"id": 0,
                       "name": "Name of the Group Configuration",
                       "description": "Description of the group configuration.",
                       "version": 1,
                       "groups": [{"id": 0,
                                   "name": "Group 1",
                                   "version": 1},
                                  {"id": 1,
                                   "name": "Group 2",
                                   "version": 1}]
                                }
                       ]

In this example:

* The ``"id": 0`` identifies the group configuration. For XML courses, the
  value is referenced in the ``user_partition`` attribute of the
  ``<split_test>`` element in the content experiment file.
* The ``groups`` array identifies the groups to which students are randomly
  assigned. For XML courses, each group ``id`` value is referenced in the
  ``group_id_to_child`` attribute of the ``<split_test>`` element.

==========================================================
Example: Multiple Group Configurations
==========================================================

The following is an example JSON object that defines two group configurations.
The first group configuration divides students into two groups, and the second
divides students into three groups.

.. code-block:: json

    "user_partitions": [{"id": 0,
                         "name": "Name of Group Configuration 1",
                         "description": "Description of Group Configuration 1.",
                         "version": 1,
                         "groups": [{"id": 0,
                                     "name": "Group 1",
                                     "version": 1},
                                    {"id": 1,
                                     "name": "Group 2",
                                     "version": 1}]}
                        {"id": 1,
                         "name": "Name of Group Configuration 2",
                         "description": "Description of Group Configuration 2.",
                         "version": 1,
                         "groups": [{"id": 0,
                                     "name": "Group 1",
                                     "version": 1},
                                    {"id": 1,
                                     "name": "Group 2",
                                     "version": 1}
                                     {"id": 2,
                                     "name": "Group 3",
                                     "version": 1}
                                     ]}
                       ]

.. note:: 
  As this example shows, each group configuration is independent.  Group IDs
  and names must be unique within a group configuration, but not across all
  group configurations in your course.