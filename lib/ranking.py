def get_score(points, hours, comments):
    return (points + (comments / 4)) / pow(hours + 2, 0.5) * 128

def get_topic_score(topic):
    return 0
