import os
import asyncio
import edge_tts
import google.generativeai as genai
from moviepy.editor import ImageClip, AudioFileClip

# Google API Key එක setup කිරීම
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def generate_script(topic):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Write a 30-second YouTube Short script about '{topic}' in Sinhala. Use an engaging and energetic tone."
    response = model.generate_content(prompt)
    return response.text

async def generate_voice(text):
    # Edge-TTS භාවිතයෙන් හඬ ගොනුවක් සෑදීම
    communicate = edge_tts.Communicate(text, "si-LK-DilaniNeural")
    await communicate.save("voice.mp3")
    print("Voice file (voice.mp3) generated successfully!")

async def create_video():
    # වීඩියෝව සහ ශබ්දය එකතු කිරීම
    # මතක තබා ගන්න: Repo එකේ 'background.jpg' නමින් පින්තූරයක් තිබිය යුතුය
    audio_clip = AudioFileClip("voice.mp3")
    image_clip = ImageClip("background.jpg").set_duration(audio_clip.duration)
    
    video = image_clip.set_audio(audio_clip)
    
    # වීඩියෝව Save කිරීම
    video.write_videofile("output.mp4", fps=24)
    print("Video generated successfully: output.mp4")

async def main():
    topic = "Amazing Science Facts"
    print("Generating script...")
    script = await generate_script(topic)
    print(f"Script: {script}")
    
    print("Generating voice...")
    await generate_voice(script)
    
    print("Creating video...")
    await create_video()

if __name__ == "__main__":
    asyncio.run(main())
