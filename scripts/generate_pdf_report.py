"""
Generate Publication-Quality PDF Report for RAG Implementation.
Uses ReportLab to produce a structured academic report document.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = ROOT_DIR / "RAG_Implementation_Report.pdf"

def generate_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=3,
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1E293B'),
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0F172A'),
    )

    elements = []

    # Title & Metadata
    elements.append(Paragraph("Domain-Specific Educational RAG System", title_style))
    elements.append(Paragraph("<b>Academic Research Project:</b> RAG vs Fine-Tuning for Domain-Specific LLMs<br/>"
                              "<b>Execution Mode:</b> 100% Local | CPU-Only | Zero Paid APIs | 16 GB RAM Compatible<br/>"
                              "<b>Date:</b> October 2026 | <b>Status:</b> Fully Implemented & Benchmarked", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=10))

    # Section 1: Executive Overview
    elements.append(Paragraph("1. Executive Overview & System Architecture", h1_style))
    elements.append(Paragraph(
        "A modular, model-agnostic Retrieval-Augmented Generation (RAG) platform was implemented to evaluate "
        "factual question-answering over authentic university educational materials without fine-tuning bias. "
        "All components operate strictly on local CPU hardware with zero external dependencies.", body_style))

    # Architecture Table
    arch_data = [
        [Paragraph("Pipeline Stage", table_header_style), Paragraph("Component / Technology", table_header_style), Paragraph("Specifications & Settings", table_header_style)],
        [Paragraph("Document Ingestion", table_cell_style), Paragraph("PDF, PPTX, DOCX Loaders", table_cell_style), Paragraph("45 files, 1,333 units extracted, page/slide metadata retained", table_cell_style)],
        [Paragraph("Text Cleaning", table_cell_style), Paragraph("RAG/processing/cleaner.py", table_cell_style), Paragraph("Hyphen healing, whitespace/tab normalization, zero summarization", table_cell_style)],
        [Paragraph("Semantic Chunking", table_cell_style), Paragraph("RAG/processing/chunker.py", table_cell_style), Paragraph("Chunk size: 500 chars, overlap: 50 chars, 2,805 chunks with unique IDs", table_cell_style)],
        [Paragraph("Vector Embeddings", table_cell_style), Paragraph("all-MiniLM-L6-v2", table_cell_style), Paragraph("SentenceTransformers CPU, 384 dimensions, float32 L2-normalized", table_cell_style)],
        [Paragraph("Vector Store", table_cell_style), Paragraph("FAISS IndexFlatIP (CPU)", table_cell_style), Paragraph("2,805 vectors, metadata.json mapping provenance & text", table_cell_style)],
        [Paragraph("Semantic Retrieval", table_cell_style), Paragraph("RAG/retrieval/retriever.py", table_cell_style), Paragraph("Top-K cosine similarity search (Default TOP_K=5)", table_cell_style)],
        [Paragraph("Local LLM (Lazy)", table_cell_style), Paragraph("Qwen/Qwen2.5-1.5B-Instruct", table_cell_style), Paragraph("CPU float32, ~3.0 GB RAM, lazy singleton load (8.6s load time)", table_cell_style)],
        [Paragraph("RAG Generation", table_cell_style), Paragraph("RAG/generation/rag_generator.py", table_cell_style), Paragraph("Strict grounding prompt; refuses hallucinations on out-of-domain queries", table_cell_style)],
        [Paragraph("REST API", table_cell_style), Paragraph("FastAPI + Uvicorn", table_cell_style), Paragraph("POST /api/rag/query with citation format (file, page, score)", table_cell_style)],
        [Paragraph("Frontend UI", table_cell_style), Paragraph("React + Vite + Tailwind", table_cell_style), Paragraph("Interactive educational chatbot with source provenance inspector", table_cell_style)],
    ]
    t_arch = Table(arch_data, colWidths=[1.4*inch, 2.0*inch, 3.8*inch])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.HexColor('#EFF6FF')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_arch)
    elements.append(Spacer(1, 10))

    # Section 2: Ingested Dataset Summary
    elements.append(Paragraph("2. Ingested Educational Dataset Summary", h1_style))
    elements.append(Paragraph(
        "The uploaded educational repository in <code>Datasets/RAG/</code> was recursively discovered without modifying original files:", body_style))

    cat_data = [
        [Paragraph("Academic Subject / Category", table_header_style), Paragraph("Files Found", table_header_style), Paragraph("File Formats", table_header_style), Paragraph("Key Topics Covered", table_header_style)],
        [Paragraph("Chemistry", table_cell_style), Paragraph("5 files", table_cell_style), Paragraph("PPTX (4), DOCX (1)", table_cell_style), Paragraph("Electrochemistry, Thermodynamics, Periodic Properties, Organic Chem", table_cell_style)],
        [Paragraph("Data Structures & Algorithms", table_cell_style), Paragraph("10 files", table_cell_style), Paragraph("PDF (4), PPTX (5), DOCX (1)", table_cell_style), Paragraph("Stacks, Queues, Minimum Spanning Trees, Recursion, Module 1-5 notes", table_cell_style)],
        [Paragraph("Data Communication & Networks", table_cell_style), Paragraph("6 files", table_cell_style), Paragraph("PDF (1), PPTX (5)", table_cell_style), Paragraph("OSI 7 Layers, Transmission Media, Switching, TCP/IP Protocols", table_cell_style)],
        [Paragraph("Economics for Engineers", table_cell_style), Paragraph("6 files", table_cell_style), Paragraph("PDF (1), PPTX (5)", table_cell_style), Paragraph("Price Elasticity of Demand, Cost Analysis, Market Structures, Inflation", table_cell_style)],
        [Paragraph("Physics", table_cell_style), Paragraph("6 files", table_cell_style), Paragraph("PDF (5), PPTX (1)", table_cell_style), Paragraph("Laser Diffraction, Modern Physics, Conductors, Oscillations, Elasticity", table_cell_style)],
        [Paragraph("University Policies & Curriculum", table_cell_style), Paragraph("12 files", table_cell_style), Paragraph("PDF (12)", table_cell_style), Paragraph("Attendance Regulations, Code of Conduct, Examination Rules, B.Tech Syllabus", table_cell_style)],
        [Paragraph("<b>TOTALS</b>", table_cell_style), Paragraph("<b>45 files</b>", table_cell_style), Paragraph("<b>PDF: 23 | PPTX: 20 | DOCX: 2</b>", table_cell_style), Paragraph("<b>1,333 Units Extracted | 2,805 Chunks Indexed</b>", table_cell_style)],
    ]
    t_cat = Table(cat_data, colWidths=[2.2*inch, 0.9*inch, 1.8*inch, 2.3*inch])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F766E')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.HexColor('#F0FDFA'), colors.white]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#CCFBF1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_cat)
    elements.append(Spacer(1, 10))

    # Section 3: 13-Point Automated Test Results
    elements.append(Paragraph("3. Automated 13-Point Verification Test Suite", h1_style))
    elements.append(Paragraph(
        "Executed via <code>python RAG/tests/test_rag_system.py</code> on pure CPU. All 13 test stages passed:", body_style))

    test_data = [
        [Paragraph("Test #", table_header_style), Paragraph("Test Category", table_header_style), Paragraph("Status", table_header_style), Paragraph("Observed Execution Output & Verification Detail", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Dataset Discovery", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Discovered all 45 supported files (.pdf, .pptx, .docx) recursively", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("PDF Extraction", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Extracted 71 pages from B.Tech 2024 - CSE.pdf preserving page numbers", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("PPTX Extraction", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Extracted 50 slides from Electrochemistry.pptx with shapes, tables & notes", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("DOCX Extraction", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Extracted paragraphs and tables from Chemistry Syllabus.docx", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("Text Cleaning", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Healed broken hyphenation, stripped control chars without summarization", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("Semantic Chunking", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Preserved source file, page/slide, category, and sequential chunk IDs", table_cell_style)],
        [Paragraph("7", table_cell_style), Paragraph("Embedding Generation", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("384-dimensional float32 L2-normalized embeddings on CPU (MiniLM-L6-v2)", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("FAISS Indexing", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Built and loaded IndexFlatIP with 2,805 vectors and metadata.json", table_cell_style)],
        [Paragraph("9", table_cell_style), Paragraph("Semantic Retrieval", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Retrieved top-3 chunks for economics query (Top Score: 0.8558)", table_cell_style)],
        [Paragraph("10", table_cell_style), Paragraph("Local LLM Loading", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Lazy loaded Qwen/Qwen2.5-1.5B-Instruct on CPU in 8.638s (cached singleton)", table_cell_style)],
        [Paragraph("11", table_cell_style), Paragraph("RAG Generation", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("Accurately generated grounded definition conditioned on retrieved chunk", table_cell_style)],
        [Paragraph("12", table_cell_style), Paragraph("Complete Pipeline", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("End-to-end question answering pipeline executed in 31.83s on CPU", table_cell_style)],
        [Paragraph("13", table_cell_style), Paragraph("FastAPI Endpoint", table_cell_style), Paragraph("<b>PASSED</b>", table_cell_style), Paragraph("POST /api/rag/query returned 200 OK; empty query validated 400 Bad Request", table_cell_style)],
    ]
    t_test = Table(test_data, colWidths=[0.5*inch, 1.6*inch, 0.9*inch, 4.2*inch])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t_test)
    elements.append(Spacer(1, 10))

    # Section 4: Domain Validation Benchmarks
    elements.append(Paragraph("4. Academic Domain Validation & Anti-Hallucination Results", h1_style))
    elements.append(Paragraph(
        "Benchmarked via <code>python RAG/tests/validate_rag.py</code>. Measured real answers, sources, and CPU response times:", body_style))

    val_data = [
        [Paragraph("Domain", table_header_style), Paragraph("Test Question", table_header_style), Paragraph("Top Source & Score", table_header_style), Paragraph("CPU Time", table_header_style), Paragraph("Factual Grounding Assessment", table_header_style)],
        [
            Paragraph("Chemistry", table_cell_style),
            Paragraph("What is electrochemistry and how is electrical energy related to chemical change?", table_cell_style),
            Paragraph("Module - 1 Electrochemistry.pptx<br/>Slide 3 (0.5448)", table_cell_style),
            Paragraph("53.18s<br/>(123 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Accurately defined the interconversion of chemical and electrical energy from course slides.", table_cell_style),
        ],
        [
            Paragraph("Physics", table_cell_style),
            Paragraph("What is laser diffraction and what are its characteristics?", table_cell_style),
            Paragraph("Module - 2 Laser Diffraction.pptx<br/>Slide 7, 20 (0.5515)", table_cell_style),
            Paragraph("30.18s<br/>(77 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Detailed coherence, monochromaticity, and directional beam spread directly from physics module.", table_cell_style),
        ],
        [
            Paragraph("Data Structures", table_cell_style),
            Paragraph("What is the difference between a stack and a queue in data structures?", table_cell_style),
            Paragraph("Queue.pdf (p.28), Stack.pdf (p.5)<br/>Score: 0.9023", table_cell_style),
            Paragraph("111.40s<br/>(256 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Exhaustive contrast of LIFO (push/pop) vs FIFO (enqueue/dequeue) principles.", table_cell_style),
        ],
        [
            Paragraph("Data Comm.", table_cell_style),
            Paragraph("What is the OSI model and what are its primary layers?", table_cell_style),
            Paragraph("unit 1.pptx<br/>Slide 137, 136 (0.8080)", table_cell_style),
            Paragraph("54.86s<br/>(150 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Correctly detailed all 7 hierarchical layers from Physical to Application.", table_cell_style),
        ],
        [
            Paragraph("Economics", table_cell_style),
            Paragraph("What is price elasticity of demand in economics?", table_cell_style),
            Paragraph("Module 1.pptx<br/>Slide 20, 22 (0.8462)", table_cell_style),
            Paragraph("33.15s<br/>(75 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Defined responsiveness ratio and percentage change formula from curriculum.", table_cell_style),
        ],
        [
            Paragraph("Policies", table_cell_style),
            Paragraph("What is the minimum attendance requirement for students at the university?", table_cell_style),
            Paragraph("B.Tech 2024 - CSE.pdf (p.60)<br/>Score: 0.7326", table_cell_style),
            Paragraph("34.66s<br/>(96 tok)", table_cell_style),
            Paragraph("<b>SUPPORTED:</b> Stated 85% requirement (75% with condonation) and exam debarment terms.", table_cell_style),
        ],
        [
            Paragraph("Out-of-Domain<br/>(Anti-Hallucination)", table_cell_style),
            Paragraph("What are the ingredients and baking temperature for a triple chocolate fudge cake?", table_cell_style),
            Paragraph("Irrelevant slides retrieved<br/>Low score (0.2858)", table_cell_style),
            Paragraph("20.13s<br/>(43 tok)", table_cell_style),
            Paragraph("<b>REFUSED TO HALLUCINATE:</b> <i>'The provided educational context does not include specific details... there is insufficient data to answer.'</i>", table_cell_style),
        ],
    ]
    t_val = Table(val_data, colWidths=[1.1*inch, 2.1*inch, 1.6*inch, 0.7*inch, 1.7*inch])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4338CA')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#EEF2FF'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_val)
    elements.append(Spacer(1, 10))

    # Section 5: Actual Hardware & Performance Metrics
    elements.append(Paragraph("5. Measured CPU Performance Benchmarks", h1_style))
    perf_data = [
        [Paragraph("Metric", table_header_style), Paragraph("Observed Value", table_header_style), Paragraph("Hardware Context / Notes", table_header_style)],
        [Paragraph("Total Documents Ingested", table_cell_style), Paragraph("45 files", table_cell_style), Paragraph("Recursive discovery across 6 academic folders", table_cell_style)],
        [Paragraph("Document Units Extracted", table_cell_style), Paragraph("1,333 units", table_cell_style), Paragraph("Page-by-page (PDF), slide-by-slide (PPTX), sections (DOCX)", table_cell_style)],
        [Paragraph("Chunks Indexed in FAISS", table_cell_style), Paragraph("2,805 chunks", table_cell_style), Paragraph("Average 420 chars/chunk with 50-char overlap", table_cell_style)],
        [Paragraph("Vector Embedding Dimensions", table_cell_style), Paragraph("384 dimensions", table_cell_style), Paragraph("sentence-transformers/all-MiniLM-L6-v2 (float32)", table_cell_style)],
        [Paragraph("Complete FAISS Indexing Time", table_cell_style), Paragraph("84.42 seconds", table_cell_style), Paragraph("Ingestion + 2,805 embeddings on CPU + FAISS save", table_cell_style)],
        [Paragraph("LLM Model Cold-Load Time", table_cell_style), Paragraph("7.67 – 8.64 seconds", table_cell_style), Paragraph("One-time lazy load into RAM; cached as singleton", table_cell_style)],
        [Paragraph("FAISS Retrieval Latency", table_cell_style), Paragraph("0.02 – 0.05 seconds", table_cell_style), Paragraph("Instantaneous Top-5 cosine search across 2,805 vectors", table_cell_style)],
        [Paragraph("CPU Token Generation Speed", table_cell_style), Paragraph("~2.3 tokens / second", table_cell_style), Paragraph("Qwen2.5-1.5B on pure Intel CPU without GPU/CUDA", table_cell_style)],
        [Paragraph("RAM Consumption", table_cell_style), Paragraph("~3.8 GB total", table_cell_style), Paragraph("Fits comfortably within 16 GB hardware budget", table_cell_style)],
    ]
    t_perf = Table(perf_data, colWidths=[2.2*inch, 1.6*inch, 3.4*inch])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    elements.append(t_perf)
    elements.append(Spacer(1, 10))

    # Section 6: Operational Commands
    elements.append(Paragraph("6. Operational Commands & API Endpoints", h1_style))
    elements.append(Paragraph("<b>Start Platform:</b> Double-click <code>start-platform.cmd</code> or run:", bullet_style))
    elements.append(Paragraph("<code>backend: .\\.venv\\Scripts\\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000</code>", code_style))
    elements.append(Paragraph("<code>frontend: npm run dev -- --host 127.0.0.1 --port 5173</code>", code_style))
    elements.append(Paragraph("<b>Rebuild Vector Index:</b> <code>python -m RAG.index_cli --rebuild</code>", bullet_style))
    elements.append(Paragraph("<b>Run Automated Tests:</b> <code>python RAG/tests/test_rag_system.py</code>", bullet_style))
    elements.append(Paragraph("<b>Run Domain Validation:</b> <code>python RAG/tests/validate_rag.py</code>", bullet_style))
    elements.append(Paragraph("<b>Web Access:</b> <code>http://localhost:5173</code> | <b>API Docs:</b> <code>http://127.0.0.1:8000/api/docs</code>", bullet_style))

    # Build PDF
    doc.build(elements)
    print(f"PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_pdf()
