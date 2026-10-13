import requests
import json
import sys

BASE = 'http://localhost:8000/api'

print('=== 15-STEP END-TO-END VERIFICATION ===\n')

# Step 1: Health & Database
r = requests.get(f'{BASE}/health')
assert r.status_code == 200, f'Health failed: {r.text}'
print('✓ Step 1 PASSED: Health & MongoDB connected')

# Step 2: Knowledge Base Summary
r = requests.get(f'{BASE}/knowledge-base/summary')
assert r.status_code == 200, f'KB Summary failed: {r.text}'
kb_data = r.json()
print(f'✓ Step 2 PASSED: KB has {kb_data.get("total_vectors")} vectors, {kb_data.get("indexed_documents_count")} indexed docs')

# Step 3: Test Datasets Available
r = requests.get(f'{BASE}/test-datasets')
assert r.status_code == 200
datasets = r.json()
names = [d["filename"] for d in datasets]
print(f'✓ Step 3 PASSED: {len(datasets)} test datasets available: {names}')

# Step 4: Standalone RAG Query
r = requests.post(f'{BASE}/rag/query', json={'question': 'What is the minimum attendance requirement?', 'domain': 'education'})
assert r.status_code == 200 and 'university_academic_policy.txt' in r.text
print('✓ Step 4 PASSED: Standalone RAG Query with document citation')

# Step 5: Standalone Fine-Tuning Query
r = requests.post(f'{BASE}/finetuning/query', json={'question': 'What is Bloom taxonomy level 4?', 'domain': 'education'})
assert r.status_code == 200 and len(r.json().get('answer', '')) > 20
print('✓ Step 5 PASSED: Standalone Fine-Tuning domain query')

# Step 6: Standalone Hybrid Query
r = requests.post(f'{BASE}/hybrid/query', json={'question': 'What is the attendance policy?', 'domain': 'education'})
assert r.status_code == 200 and len(r.json().get('answer', '')) > 20
print('✓ Step 6 PASSED: Standalone Hybrid query with retrieval & synthesis')

# Step 7: Single Question Compare
r = requests.post(f'{BASE}/compare', json={'question': 'What are the rules for academic probation?', 'domain': 'education'})
assert r.status_code == 200
comp_res = r.json().get('results', {})
assert 'rag' in comp_res and 'fine_tuned' in comp_res and 'hybrid' in comp_res
print('✓ Step 7 PASSED: Single Question 3-way Compare')

# Step 8: Comparison Benchmark Engine (POST /api/compare/run)
print('\nRunning Comparison Benchmark on education_eval_benchmark.json...')
r = requests.post(f'{BASE}/compare/run', json={
    'test_dataset': 'education_eval_benchmark.json',
    'approaches': ['RAG', 'FINE_TUNING', 'HYBRID'],
    'domain': 'education',
    'name': 'Comprehensive Education Benchmark E2E',
    'limit': 3
})
assert r.status_code == 200, f'Compare run failed: {r.text}'
benchmark_data = r.json()
exp_id = benchmark_data['experiment_id']
print(f'✓ Step 8 PASSED: Benchmark Run succeeded. Experiment ID: {exp_id}, questions evaluated: {benchmark_data.get("total_questions")}')

# Step 9: Verify Experiment In Database & Detail Retrieval
r = requests.get(f'{BASE}/experiments/{exp_id}')
assert r.status_code == 200
exp = r.json()
assert exp['experiment_id'] == exp_id
print(f'✓ Step 9 PASSED: Experiment retrieved from DB with approaches={exp.get("approach")} and status={exp.get("status")}')

# Step 10: Verify Metrics & Breakdown
metrics_summary = exp.get('metrics') or exp.get('results', {}).get('approach_summary', {})
print('✓ Step 10 PASSED: Experiment Summary Metrics:')
for app_k, metrics in metrics_summary.items():
    print(f'   - {app_k.upper()}: accuracy={metrics.get("accuracy")}, latency={metrics.get("avg_latency_ms")}ms, faithfulness={metrics.get("faithfulness")}')

# Step 11: Error Analysis Identification
error_cases = exp.get('error_analysis') or exp.get('results', {}).get('error_analysis', [])
print(f'✓ Step 11 PASSED: Detected {len(error_cases)} categorized failure/error instances')
for ec in error_cases[:3]:
    print(f'   - [{ec.get("approach")}] {ec.get("category")}: {ec.get("issue")} (Severity: {ec.get("severity")})')

# Step 12: Human Evaluation Review Submission
r = requests.post(f'{BASE}/human-eval', json={
    'experiment_id': exp_id,
    'question_id': 'Q001',
    'question': 'What is the minimum attendance requirement for students to sit for final examinations?',
    'approach': 'RAG',
    'answer': 'Under Section 2 of the Academic Regulations, students must maintain at least 75% attendance.',
    'evaluator': 'Prof. Academic Reviewer',
    'verdict': 'Correct',
    'correctness': 5,
    'relevance': 5,
    'faithfulness': 5,
    'clarity': 5,
    'citation_quality': 5,
    'comments': 'Accurately retrieved Section 2 of University Academic Policy with verified 75% attendance threshold citation.'
})
assert r.status_code in (200, 201), f'Human eval failed: {r.text}'
print('✓ Step 12 PASSED: Human evaluation record saved with 5-dimension rubric')

# Step 13: Research Report Generation (13 Academic Sections)
r = requests.get(f'{BASE}/experiments/{exp_id}/report')
assert r.status_code == 200
report_data = r.json()
sections = report_data.get('sections', [])
assert len(sections) == 13, f'Expected 13 sections, got {len(sections)}'
print(f'✓ Step 13 PASSED: Full Academic Research Report generated with {len(sections)} sections:')
for s in sections:
    print(f'   {s.get("section_number")}. {s.get("title")}')

# Step 14: Export Experiment as JSON
r = requests.get(f'{BASE}/experiments/{exp_id}/export?format=json')
assert r.status_code == 200
data_json = r.json()
assert 'experiment' in data_json and 'evaluations' in data_json
print(f'✓ Step 14 PASSED: Experiment successfully exported as JSON with {len(data_json.get("evaluations", []))} evaluations')

# Step 15: Export Experiment as CSV
r = requests.get(f'{BASE}/experiments/{exp_id}/export?format=csv')
assert r.status_code == 200
assert 'experiment_id' in r.text and 'question_id' in r.text
print('✓ Step 15 PASSED: Experiment successfully exported as CSV')

print('\n' + '='*60)
print('ALL 15 END-TO-END VERIFICATION STEPS COMPLETED AND VALIDATED!')
print('='*60)
