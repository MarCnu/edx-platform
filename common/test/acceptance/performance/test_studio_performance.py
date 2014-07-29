"""
Single page performance tests for Studio.
"""
from bok_choy.performance import WebAppPerfReport, with_cache
from ..pages.studio.auto_auth import AutoAuthPage
from ..pages.studio.login import LoginPage
from ..pages.studio.overview import CourseOutlinePage
from ..pages.studio.signup import SignupPage
from ..pages.studio.utils import click_css, set_input_value_and_save


class StudioPagePerformanceTestExample(WebAppPerfReport):
    """
    Example test case.
    """

    @with_cache
    def test_signup_flow_with_cache(self):
        """
        Produce a report for the login --> signup page performance.

        This example will produde two har files. The first will show the performance
        of the flow when it starts from a browser with an empty cache. The second (which
        with have '_cached_2' on the end of the file name), will show the performance when
        the browser has already been through the flow once before and has cached some assets.
        """
        # Declaring a new page will instatiate a new har instance if one hasn't been already.
        self.new_page('LoginPage')

        login_page = LoginPage(self.browser)
        login_page.visit()

        # Declare that you are going to a new page first, then navigate to the next page.
        self.new_page('SignupPage')
        signup_page = SignupPage(self.browser)
        signup_page.visit()

        # Save the har file, passing it a name for the file
        self.save_har('LoginPage_and_SignupPage')

    def test_signup_flow_no_cache(self):
        """
        Produce a report for the login --> signup page performance.

        This example will produde two har files. The first will show the performance
        of the LoginPage when it starts from a browser with an empty cache. The second will show
        the performance of the SignUp page when the browser has already been to the LoginPage
        and has cached some assets.
        """

        self.new_page('LoginPage')
        login_page = LoginPage(self.browser)
        login_page.visit()

        # Save the first har file.
        # Note that saving will 'unset' the har, so that if you were to declare another new
        # page after this point, it would start recording a new har. This means that you can
        # also explitily capture many hars in a single test. See the next example.
        self.save_har('LoginPage')

        # Declare that you are going to a new page, then navigate to the next page.
        # This will start recording a new har here.
        self.new_page('SignupPage')
        signup_page = SignupPage(self.browser)
        signup_page.visit()
        # Save the second har file.
        self.save_har('SignupPage')


class StudioPagePerformanceTest(WebAppPerfReport):
    def setUp(self):
        """
        Authenticate as staff so we can view and edit courses.
        """
        super(StudioPagePerformanceTest, self).setUp()
        AutoAuthPage(self.browser, staff=True).visit()

    def record_visit_course_outline(self, course_outline_page):
        """
        Produce a performance report for visiting the course outline page.
        """
        har_name = 'perf-fixes/OutlinePage_{org}_{course}'.format(
            org=course_outline_page.course_info['course_org'],
            course=course_outline_page.course_info['course_num']
        )
        self.new_page(har_name)
        course_outline_page.visit()
        self.save_har(har_name)

    def record_visit_unit_page(self, course_outline_unit, course_info):
        """
        Produce a performance report for visiting a unit page.
        """
        har_name = 'perf-fixes/UnitPage_{org}_{course}'.format(
            org=course_info['course_org'],
            course=course_info['course_num']
        )
        self.new_page(har_name)
        course_outline_unit.go_to()
        self.save_har(har_name)

    def record_update_subsection_in_course_outline(self, course_outline_page, section_title, original_subsection_title):
        """
        Produce a performance report for updating a subsection on the
        outline page.
        """
        edited_subsection_title = "Edited Subsection Title"

        # Since this method is called twice, the subsection we want
        # will either have its original name or our edited one.
        if self.with_cache:
            subsection = course_outline_page.section(section_title).subsection(edited_subsection_title)
        else:
            subsection = course_outline_page.section(section_title).subsection(original_subsection_title)

        har_name = 'perf-fixes/OutlinePageUpdateSubsection_{org}_{course}'.format(
            org=course_outline_page.course_info['course_org'],
            course=course_outline_page.course_info['course_num']
        )
        self.new_page(har_name)
        if self.with_cache:
            subsection.change_name(original_subsection_title)
        else:
            subsection.change_name(edited_subsection_title)
        self.save_har(har_name)

    def record_publish_unit_page(self, course_outline_page, section_title, subsection_title, original_unit_title):
        """
        Produce a performance report for publishing an edited unit container page.
        """
        edited_unit_title = 'Edited Unit Title'
        if self.with_cache:
            current_unit_title = edited_unit_title
            new_unit_title = original_unit_title
        else:
            current_unit_title = original_unit_title
            new_unit_title = edited_unit_title

        container_page = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(current_unit_title).go_to()
        container_page.change_name(new_unit_title)

        har_name = 'perf-fixes/UnitPagePublish_{org}_{course}'.format(
            org=course_outline_page.course_info['course_org'],
            course=course_outline_page.course_info['course_num']
        )
        self.new_page(har_name)
        click_css(container_page, '.action-publish')
        container_page.wait_for_ajax()
        self.save_har(har_name)

    @with_cache
    def test_justice_visit_outline(self):
        """
        Produce a report for Justice's outline page performance.
        """
        self.record_visit_course_outline(CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring'))

    @with_cache
    def test_pub101_visit_outline(self):
        """
        Produce a report for Andy's PUB101 outline page performance.
        """
        self.record_visit_course_outline(CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101'))

    @with_cache
    def test_justice_update_subsection(self):
        """
        Record updating a subsection on the Justice outline page.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        self.record_update_subsection_in_course_outline(
            course_outline_page,
            'Lecture 1 - Doing the Right Thing',
            'Discussion Prompt: Ethics of Torture'
        )

    @with_cache
    def test_pub101_update_subsection(self):
        """
        Record updating a subsection on Andy's PUB101 outline page.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101')
        course_outline_page.visit()

        self.record_update_subsection_in_course_outline(
            course_outline_page,
            'Released',
            'Released'
        )

    @with_cache
    def test_justice_visit_unit_page(self):
        """
        Produce a report for the unit page performance of Justice.
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
        """
        course_outline_page = CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101')
        course_outline_page.visit()

        section_title = 'Released'
        subsection_title = 'Released'
        unit_title = subsection_title

        course_outline_unit = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(unit_title)
        self.record_visit_unit_page(course_outline_unit, course_outline_page.course_info)

    @with_cache
    def test_justice_publish_unit_page(self):
        """
        Produce a report for the performance of publishing a unit with changes on Justice.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        section_title = 'Lecture 1 - Doing the Right Thing'
        subsection_title = 'Discussion Prompt: Ethics of Torture'
        unit_title = subsection_title

        self.record_publish_unit_page(course_outline_page, section_title, subsection_title, unit_title)

    @with_cache
    def test_pub101_publish_unit_page(self):
        """
        Produce a report for the performance of publishing a unit with changes on Andy's PUB101.
        """
        course_outline_page = CourseOutlinePage(self.browser, 'AndyA', 'PUB101', 'PUB101')
        course_outline_page.visit()

        section_title = 'Released'
        subsection_title = 'Released'
        unit_title = subsection_title

        self.record_publish_unit_page(course_outline_page, section_title, subsection_title, unit_title)
