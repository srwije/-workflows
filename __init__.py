from LoginDetails import LoginDetails
from TestCases import TestCases
from Report_Generator import ReportGenerator


def main(accounts):
    for account in accounts:
        # Update login details for the current account
        login_details = LoginDetails()
        login_details.username = account['username']
        login_details.password = account['password']

        # Initialize the report generator for this account
        report = ReportGenerator(f"FleetMGT_Report_{login_details.username}")
        test_cases = TestCases(login_details)

        # Run test cases
        test_cases.login(report)
        test_cases.check_devices(report)

        # Generate and send the report
        report_name = report.generate_report()
        report.send_report_via_email(
            email_list=["ravinda.esol@gmail.com"],
            # email_list=["ravinda.esol@gmail.com", "charithv@effectivesolutions.lk", "hariharankanakaraja@gmail.com"],
            app_password="gfws euwi poai nmpo",
            sender_email="wije2582@gmail.com",
            report_name=report_name
        )


if __name__ == "__main__":
    accounts = [
        #{"username": "nolimit_admin", "password": "nolimit@123"},
        {"username": "aw_admin", "password": "aw@123"}
    ]
    main(accounts)