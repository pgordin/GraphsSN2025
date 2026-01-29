import moviepy as mp

# Load your videos
v1 = mp.VideoFileClip("./media/videos/main/1080p60/GraphColoring.mp4")
v2 = mp.VideoFileClip("./media/videos/main/1080p60/GraphFlip.mp4")
v3 = mp.VideoFileClip("./media/videos/main/1080p60/GraphColoring4Colors.mp4")

# Concatenate in order
final = mp.concatenate_videoclips([v1, v2, v3])

# Export result
final.write_videofile("final.mp4", codec="libx264", audio_codec="aac")