from .models import TimeFrame

def get_list_time_frames_by_field_id(field_id: int) -> list[TimeFrame]:
    return TimeFrame.query.filter_by(field_id=field_id).all()