"""
Single page performance tests for Studio.
"""
from bok_choy.performance import WebAppPerfReport, with_cache
from ..pages.studio.auto_auth import AutoAuthPage
from ..pages.studio.login import LoginPage
from ..pages.studio.overview import CourseOutlinePage
from ..pages.studio.signup import SignupPage
from ..pages.studio.utils import click_css, set_input_value_and_save


class StudioPagePerformanceTest(WebAppPerfReport):
    """
    Capture studio performance with HTTP Archives.
    """
    def setUp(self):
        """
        Authenticate as staff so we can view and edit courses.
        """
        super(StudioPagePerformanceTest, self).setUp()
        AutoAuthPage(self.browser, staff=True).visit()

    def record_visit_course_outline(self, course_outline_page):
        """
        Produce a HAR for loading the course outline page.
        """
        har_name = 'OutlinePage_{org}_{course}'.format(
            org=course_outline_page.course_info['course_org'],
            course=course_outline_page.course_info['course_num']
        )
        self.new_page(har_name)
        course_outline_page.visit()
        self.save_har(har_name)

    def record_visit_unit_page(self, course_outline_unit, course_info):
        """
        Produce a HAR for loading a unit page.
        """
        har_name = 'UnitPage_{org}_{course}'.format(
            org=course_info['course_org'],
            course=course_info['course_num']
        )
        self.new_page(har_name)
        course_outline_unit.go_to()
        self.save_har(har_name)

    @with_cache
    def test_justice_visit_outline(self):
        """
        Produce a report for Justice's outline page performance.

        This method assumes that HarvardX's Justice exists in the bok choy database.
        """
        self.record_visit_course_outline(CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring'))

    @with_cache
    def test_pub101_visit_outline(self):
        """
        Produce a report for Andy's PUB101 outline page performance.

        This method assumes that Andy's Publishing 101 exists the bok choy database.
        """
        self.record_visit_course_outline(CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101'))

    @with_cache
    def test_justice_visit_unit_page(self):
        """
        Produce a report for the unit page performance of Justice.

        This method assumes that HarvardX's Justice exists in the bok choy database.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        section_title = 'Lecture 1 - Doing the Right Thing'
        subsection_title = 'Discussion Prompt: Ethics of Torture'
        unit_title = subsection_title

        course_outline_unit = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(unit_title)
        self.record_visit_unit_page(course_outline_unit, course_outline_page.course_info)

    @with_cache
    def test_pub101_visit_unit_page(self):
        """
        Produce a report for the unit page performance of Andy's PUB101.

        This method assumes that Andy's Publishing 101 exists the bok choy database.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101')
        course_outline_page.visit()

        section_title = 'Released'
        subsection_title = 'Released'
        unit_title = subsection_title

        course_outline_unit = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(unit_title)
        self.record_visit_unit_page(course_outline_unit, course_outline_page.course_info)
