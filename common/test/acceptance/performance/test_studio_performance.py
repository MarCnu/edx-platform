"""
Single page performance tests for Studio.
"""
from bok_choy.performance import WebAppPerfReport, with_cache
from ..pages.studio.auto_auth import AutoAuthPage
from ..pages.studio.container import ContainerPage
from ..pages.studio.login import LoginPage
from ..pages.studio.overview import CourseOutlinePage
from ..pages.studio.signup import SignupPage


class StudioPagePerformanceTest(WebAppPerfReport):
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

    @with_cache
    def test_visit_course_outline_with_cache(self):
        """
        Produce a report for the outline page performance.
        """
        auth_page = AutoAuthPage(self.browser, staff=True)
        auth_page.visit()
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')

        self.new_page('OutlinePage')
        course_outline_page.visit()
        self.save_har('OutlinePage')

    @with_cache
    def test_update_subsection_in_course_outline_with_cache(self):
        """
        Produce a report for the performance of updating a subsection
        on the outline page.
        """
        auth_page = AutoAuthPage(self.browser, staff=True)
        auth_page.visit()
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        section_title = 'Lecture 1 - Doing the Right Thing'
        initial_subsection_title = 'Discussion Prompt: Ethics of Torture'
        edited_subsection_title = 'New Subsection Title'

        if self.with_cache:
            subsection = course_outline_page.section(section_title).subsection(edited_subsection_title)
        else:
            subsection = course_outline_page.section(section_title).subsection(initial_subsection_title)

        self.new_page('OutlinePageUpdateSubsection')
        # Since this test is run twice, (second time cached), we need
        # to have a different name each time, otherwise the edit won't
        # go through
        if self.with_cache:
            subsection.change_name(initial_subsection_title)
        else:
            subsection.change_name(edited_subsection_title)
        self.save_har('OutlinePageUpdateSubsection')

    @with_cache
    def test_visit_unit_page_with_cache(self):
        """
        Produce a report for the unit page performance.
        """
        auth_page = AutoAuthPage(self.browser, staff=True)
        auth_page.visit()
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        section_title = 'Lecture 1 - Doing the Right Thing'
        subsection_title = 'Discussion Prompt: Ethics of Torture'
        unit_title = subsection_title

        unit = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(unit_title)

        self.new_page('UnitPage')
        unit.go_to()
        self.save_har('UnitPage')

    @with_cache
    def test_publish_unit_page_with_cache(self):
        """
        Produce a report for the performance of publishing a unit with changes.
        """
        auth_page = AutoAuthPage(self.browser, staff=True)
        auth_page.visit()
        course_outline_page = CourseOutlinePage(self.browser, 'HarvardX', 'ER22x', '2013_Spring')
        course_outline_page.visit()

        section_title = 'Lecture 1 - Doing the Right Thing'
        subsection_title = 'Discussion Prompt: Ethics of Torture'
        unit_title = subsection_title
        unit = course_outline_page.section(section_title).subsection(subsection_title).toggle_expand().unit(unit_title)
        locator = unit.locator
        unit.go_to()

        container_page = ContainerPage(self.browser, locator)
        container_page.delete(0)

        self.new_page('PublishUnitPage')
        container_page.publish_action.click()
        container_page.wait_for_ajax()
        self.save_har('PublishUnitPage')
