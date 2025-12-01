class AppProcess:
    def __init__(self, api_service, state_manager, navigator):
        self.api = api_service
        self.state = state_manager
        self.nav = navigator

        # Fetch job list from API service and store results in state
    def load_jobs(self):
        jobs = self.api.fetch_jobs()
        self.state.set_jobs(jobs)
        return jobs

        # User clicked on a job in the UI store selected job and navigate
    def select_job(self, job_id):
        self.state.set_selected_job(job_id)
        self.nav.go_to("upload_page")

        # Resume uploaded in the GUI store files and move to review screen
    def upload_files(self, files):
        self.state.set_files(files)
        self.nav.go_to("review_page")

        # Final submit: send data to API, clear temporary state, then navigate
    def submit_application(self):
        job_id = self.state.get_selected_job()
        files = self.state.get_files()
        response = self.api.submit_application(job_id, files)
        self.state.clear_files()
        self.nav.go_to("confirmation_page")
        return response

        # Called by the UI Back button uses Navigator to go back
    def back(self):
        self.nav.back()
