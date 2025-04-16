# MarkeOS Course Analyzer Package
from .course_analyzer import CourseAnalyzer, CourseAnalysisRequest, CourseAnalysisResponse
from .utils.check_env import check_env

__version__ = "0.1.0"

__all__ = [
    'CourseAnalyzer',
    'CourseAnalysisRequest',
    'CourseAnalysisResponse',
    'check_env'
]