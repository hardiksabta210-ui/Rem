from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from pathlib import Path
from datetime import datetime

desktop_path = Path.home() / 'Desktop' / 'REM_OpenClaw_Workflow.pdf'
pdf = SimpleDocTemplate(str(desktop_path), pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1f4788'), spaceAfter=12, alignment=TA_CENTER)
heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0066cc'), spaceAfter=8)
body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, alignment=TA_JUSTIFY, spaceAfter=6)

story = []
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph('REM + OPENCLAW', title_style))
story.append(Paragraph('Complete Workflow Documentation', styles['Heading2']))
story.append(Spacer(1, 0.2*inch))
gen_date = datetime.now().strftime('%B %d, %Y')
story.append(Paragraph(f'Generated: {gen_date}', body_style))
story.append(PageBreak())

story.append(Paragraph('TABLE OF CONTENTS', heading_style))
contents = ['1. Project Overview', '2. System Architecture', '3. Voice Pipeline', '4. OpenClaw Integration', '5. Key Components', '6. Communication Flow', '7. Startup Process', '8. API Endpoints', '9. Examples', '10. Troubleshooting']
for item in contents:
    story.append(Paragraph(item, body_style))
story.append(PageBreak())

story.append(Paragraph('1 - PROJECT OVERVIEW', heading_style))
overview = 'REM is a local AI assistant with voice, LLM, TTS, ASR, and web control. It integrates with OpenClaw for multi-channel AI operations.'
story.append(Paragraph(overview, body_style))
story.append(Paragraph('Features: LLM (Ollama) | TTS (SoVITS) | ASR (Whisper) | Web Control | Chat with Memory', body_style))
story.append(PageBreak())

story.append(Paragraph('2 - SYSTEM ARCHITECTURE', heading_style))
arch_items = [
    'Layer 1: Voice Interface (Microphone) to Whisper ASR',
    'Layer 2: Text Understanding via Ollama LLM',
    'Layer 3: Routing via Intent Detection',
    'Layer 4: Execution through Services',
    'Layer 5: Response via SoVITS TTS to Speaker',
    'Layer 6: Integration via OpenClaw Bridge HTTP API'
]
for item in arch_items:
    story.append(Paragraph(item, body_style))
story.append(PageBreak())

story.append(Paragraph('3 - VOICE PROCESSING PIPELINE', heading_style))
pipeline_steps = [
    '1. User Speaks: "Open YouTube and search for Python"',
    '2. Whisper ASR: Converts audio to text',
    '3. Ollama LLM: Processes and understands intent',
    '4. Intent Detection: youtube_search + "python"',
    '5. Browser Automation: Opens YouTube search',
    '6. TTS: "Done, sir. YouTube search opened."',
    '7. Playback: User hears confirmation',
    '8. Loop: Ready for next command'
]
for step in pipeline_steps:
    story.append(Paragraph(step, body_style))
story.append(PageBreak())

story.append(Paragraph('4 - OPENCLAW INTEGRATION', heading_style))
services = 'Services: LLM_GENERATE | LLM_CHAT | TTS_GENERATE | ASR_TRANSCRIBE | WEB_CONTROL | VOICE_WAKE | HEALTH_CHECK'
story.append(Paragraph(services, body_style))
story.append(Paragraph('HTTP Bridge: openclaw_bridge.py on port 8765', body_style))
story.append(Paragraph('API Format: REST POST requests with JSON responses', body_style))
story.append(PageBreak())

story.append(Paragraph('5 - KEY COMPONENTS', heading_style))
components = [
    ['Component', 'Purpose'],
    ['main_chat.py', 'Main voice orchestration'],
    ['rem_openclaw_adapter.py', 'REM to OpenClaw bridge'],
    ['api_server_robust.py', 'REM API with dynamic ports'],
    ['bridge_server_robust.py', 'HTTP gateway'],
    ['web_control.py', 'Intent detection'],
    ['launcher.py', 'One-command startup'],
]
comp_table = Table(components, colWidths=[2*inch, 3*inch])
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
]))
story.append(comp_table)
story.append(PageBreak())

story.append(Paragraph('6 - SERVICE COMMUNICATION', heading_style))
story.append(Paragraph('Method 1 (Direct): In-process, fastest for voice', body_style))
story.append(Paragraph('Method 2 (HTTP): External apps via REST API', body_style))
story.append(Paragraph('Method 3 (CLI): Command-line interface', body_style))
story.append(PageBreak())

story.append(Paragraph('7 - STARTUP PROCESS', heading_style))
story.append(Paragraph('Command: python launcher.py', body_style))
story.append(Paragraph('Actions: Kills existing → Verifies ports → Starts API (8000) → Bridge (8765) → Voice Chat', body_style))
story.append(Paragraph('Dynamic Ports: Tries fallback ports if defaults busy', body_style))
story.append(PageBreak())

story.append(Paragraph('8 - API ENDPOINTS', heading_style))
endpoints = [
    ['Endpoint', 'Method', 'Purpose'],
    ['/health', 'GET', 'Check status'],
    ['/llm/generate', 'POST', 'Generate text'],
    ['/web/control', 'POST', 'Web control'],
    ['/tts/generate', 'POST', 'Speech synthesis'],
]
ep_table = Table(endpoints, colWidths=[1.8*inch, 1*inch, 2.2*inch])
ep_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.blue),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
]))
story.append(ep_table)
story.append(PageBreak())

story.append(Paragraph('9 - WORKFLOW EXAMPLES', heading_style))
story.append(Paragraph('Voice: Speak command → Whisper → LLM → Web/TTS → Output', body_style))
story.append(Paragraph('HTTP: POST /web/control → Browser action → JSON response', body_style))
story.append(Paragraph('CLI: rem web "search youtube" → Immediate execution', body_style))
story.append(PageBreak())

story.append(Paragraph('10 - TROUBLESHOOTING', heading_style))
story.append(Paragraph('Services wont start: Close windows, run launcher again', body_style))
story.append(Paragraph('Port conflicts: Dynamic allocation handles it', body_style))
story.append(Paragraph('Ollama missing: Optional, install separately', body_style))
story.append(Paragraph('Audio issues: Check microphone and FFmpeg', body_style))

pdf.build(story)
print(f'PDF created: {desktop_path}')
print('Open on Desktop: REM_OpenClaw_Workflow.pdf')
