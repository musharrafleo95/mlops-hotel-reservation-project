import traceback

class CustomException(Exception):
    def __init__(self, error_message: str, exc: Exception):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, exc)

    @staticmethod
    def get_detailed_error_message(error_message: str, exc: Exception) -> str:
        
        # _, _, exc_tb = error_detail.exc_info() # getting exception traceback
        # file_name = exc_tb.tb_frame.f_code.co_filename # getting file name
        # line_number = exc_tb.tb_lineno # getting line number of a error

        # return f"Error in {file_name}, line {line_number} : {error_message}"

        tb = exc.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        file_name = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        return f"Error in {file_name}, line {line_number}: {error_message} | Original: {exc}"
    
    def __str__(self):
        """gives a text representation of the error message -> str(e)"""
        return self.error_message
