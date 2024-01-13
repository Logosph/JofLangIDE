import python.domain.ApplicationRunUseCase as ApplicationRunUseCase

class MainWindowPresenter:
    def button_clicked(self):
        print("Test Button")  # use case

    def run_button_clicked(self):
        ApplicationRunUseCase.execute()


