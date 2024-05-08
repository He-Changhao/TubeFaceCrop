### Project Overview
TubeFaceCrop is a tool for crawling videos related to keywords from YouTube and preprocessing them. It is based on [MTCNN](https://github.com/ipazc/mtcnn?tab=readme-ov-file) to automatically remove faces from the videos and perform central crop, and finally segments the videos into 5-second clips for further processing and analysis.

### Usage
1. **Clone the project locally**:
   ```
   git clone https://github.com/He-Changhao/TubeFaceCrop.git
   ```

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Run the main program**:
   ```
   python main.py
   ```

### Features
- Crawls related videos from YouTube based on a list of user keywords in the name.xlsx file.
- Automatically detects and removes faces from videos, with adjustable detection frequency.
- Performs central crop on videos, with adjustable crop size.
- Segments videos into 5-second clips for saving.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
