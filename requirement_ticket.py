"""
Business Requirement Ticket Generator
A Streamlit application for converting unstructured text into structured business requirements
"""

import streamlit as st
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from requirement_processor import RequirementProcessor, create_ticket

# Configure page
st.set_page_config(
	page_title="Business Requirement Ticket Generator",
	page_icon="📋",
	layout="wide",
	initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
	<style>
		.requirement-true {
			background-color: #d4edda;
			border-left: 4px solid #28a745;
			padding: 12px;
			border-radius: 4px;
		}
		.requirement-false {
			background-color: #f8d7da;
			border-left: 4px solid #dc3545;
			padding: 12px;
			border-radius: 4px;
		}
		.entity-stakeholder {
			background-color: #cfe2ff;
			padding: 2px 6px;
			border-radius: 3px;
			margin: 0 2px;
		}
		.entity-action {
			background-color: #fff3cd;
			padding: 2px 6px;
			border-radius: 3px;
			margin: 0 2px;
		}
		.entity-object {
			background-color: #d1ecf1;
			padding: 2px 6px;
			border-radius: 3px;
			margin: 0 2px;
		}
		.entity-quality {
			background-color: #e2e3e5;
			padding: 2px 6px;
			border-radius: 3px;
			margin: 0 2px;
		}
		.entity-priority {
			background-color: #f8c1c1;
			padding: 2px 6px;
			border-radius: 3px;
			margin: 0 2px;
		}
		.ticket-output {
			background-color: #f8f9fa;
			border: 1px solid #dee2e6;
			padding: 16px;
			border-radius: 6px;
			font-family: 'Courier New', monospace;
		}
		.confidence-badge {
			display: inline-block;
			padding: 4px 12px;
			border-radius: 12px;
			font-weight: bold;
			color: white;
			margin: 4px 0;
		}
		.confidence-high {
			background-color: #28a745;
		}
		.confidence-medium {
			background-color: #ffc107;
			color: black;
		}
		.confidence-low {
			background-color: #dc3545;
		}
	</style>
""", unsafe_allow_html=True)

# Initialize processor
@st.cache_resource
def load_processor():
	return RequirementProcessor()

processor = load_processor()

# Sidebar configuration
st.sidebar.title("⚙️ Configuration")
confidence_threshold = st.sidebar.slider(
	"Requirement Confidence Threshold",
	min_value=0.0,
	max_value=1.0,
	value=0.3,
	step=0.05,
	help="Minimum confidence score for text to be classified as a requirement"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
	"""
	### 📖 How it works

	1. **Input**: Paste or type unstructured text describing a business need
	2. **Analysis**: The system:
	   - Identifies if text is a business requirement
	   - Extracts key entities (stakeholder, action, object, etc.)
	   - Highlights important keywords
	   - Calculates confidence scores
	3. **Output**: Generates a structured ticket with extracted information

	### 🏷️ Entity Types
	- **STAKEHOLDER**: Who needs it (user, admin, customer, etc.)
	- **ACTION**: What to do (create, update, delete, etc.)
	- **OBJECT**: What to act upon (report, data, file, etc.)
	- **QUALITY**: Non-functional requirements (secure, scalable, etc.)
	- **PRIORITY**: Urgency level (high, medium, low)
	"""
)

# Main content
st.title("📋 Business Requirement Ticket Generator")
st.markdown(
	"Transform unstructured text into structured business requirements with automatic entity extraction and confidence scoring."
)

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
	st.subheader("📝 Input Text")
	user_text = st.text_area(
		"Paste or type your business requirement text:",
		height=250,
		placeholder="Example: We need a mobile application that allows users to track their fitness goals and progress with real-time notifications",
		key="user_input"
	)

with col2:
	st.subheader("✨ Preview")
	if user_text:
		st.markdown("**Text Preview:**")
		st.info(user_text[:200] + "..." if len(user_text) > 200 else user_text)
	else:
		st.info("Enter text to see preview...")

# Process button
if st.button("🚀 Analyze & Generate Ticket", use_container_width=True, type="primary"):
	if not user_text.strip():
		st.error("Please enter some text to analyze.")
	else:
		with st.spinner("Processing... This may take a moment..."):
			# Extract entities
			entities = processor.extract_entities(user_text)

			# Determine if it's a requirement
			is_req, req_score = processor.is_requirement(user_text, confidence_threshold)

			# Create ticket
			ticket = create_ticket(entities, is_req, req_score)

			# Store in session state for display
			st.session_state.processed_result = {
				'entities': entities,
				'is_requirement': is_req,
				'req_score': req_score,
				'ticket': ticket,
				'keywords': processor.extract_keywords(user_text),
				'highlighted_text': processor.highlight_text(user_text)
			}

# Display results if available
if 'processed_result' in st.session_state:
	result = st.session_state.processed_result
	entities = result['entities']
	is_req = result['is_requirement']
	req_score = result['req_score']
	ticket = result['ticket']
	keywords = result['keywords']
	highlighted_text = result['highlighted_text']

	st.markdown("---")
	st.subheader("📊 Analysis Results")

	# Requirement classification banner
	if is_req:
		st.markdown(
			f"""
			<div class="requirement-true">
				<h3>✅ Valid Business Requirement</h3>
				<p>This text has been identified as a business requirement with <strong>high confidence</strong>.</p>
			</div>
			""",
			unsafe_allow_html=True
		)
	else:
		st.markdown(
			f"""
			<div class="requirement-false">
				<h3>❌ Not a Business Requirement</h3>
				<p>This text does not appear to be a structured business requirement. It may be general feedback or discussion.</p>
			</div>
			""",
			unsafe_allow_html=True
		)

	# Metrics and visualizations
	col1, col2, col3, col4 = st.columns(4)

	with col1:
		st.metric("Requirement Score", f"{req_score:.0%}")

	with col2:
		st.metric("Extraction Confidence", f"{entities['confidence']:.0%}")

	with col3:
		entity_count = sum(1 for v in entities.values() if v and v != entities['originalText'])
		st.metric("Entities Found", entity_count)

	with col4:
		keyword_count = len(keywords['requirement_keywords']) + len(keywords['quality_keywords'])
		st.metric("Keywords Found", keyword_count)

	# Two column layout for detailed results
	col1, col2 = st.columns(2)

	with col1:
		st.subheader("🔍 Highlighted Text")
		st.markdown(
			"""
			<style>
				.highlighted-text { line-height: 1.8; font-size: 14px; }
				.entity-STAKEHOLDER { background-color: #cfe2ff; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-ACTION { background-color: #fff3cd; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-OBJECT { background-color: #d1ecf1; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-SYSTEM { background-color: #e7d4f5; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-QUALITY { background-color: #e2e3e5; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-PRIORITY { background-color: #f8c1c1; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-CONDITION { background-color: #d4f1f4; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
				.entity-CONSTRAINT { background-color: #f5d5f5; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
			</style>
			<div class="highlighted-text">
		""",
			unsafe_allow_html=True
		)

		# Build HTML for highlighted text
		html_text = ""
		for text_segment, label in highlighted_text:
			if label == "normal":
				html_text += text_segment
			else:
				html_text += f'<span class="entity-{label}">{text_segment}</span> '

		st.markdown(html_text + "</div>", unsafe_allow_html=True)

		# Legend
		st.markdown("**Entity Legend:**")
		legend_cols = st.columns(4)
		with legend_cols[0]:
			st.markdown('<span style="background-color: #cfe2ff; padding: 2px 6px; border-radius: 3px;">Stakeholder</span>', unsafe_allow_html=True)
		with legend_cols[1]:
			st.markdown('<span style="background-color: #fff3cd; padding: 2px 6px; border-radius: 3px;">Action</span>', unsafe_allow_html=True)
		with legend_cols[2]:
			st.markdown('<span style="background-color: #d1ecf1; padding: 2px 6px; border-radius: 3px;">Object</span>', unsafe_allow_html=True)
		with legend_cols[3]:
			st.markdown('<span style="background-color: #e2e3e5; padding: 2px 6px; border-radius: 3px;">Quality</span>', unsafe_allow_html=True)

	with col2:
		st.subheader("📈 Confidence Breakdown")

		# Create confidence gauge
		confidence_data = {
			'Requirement Score': req_score * 100,
			'Extraction Confidence': entities['confidence'] * 100,
		}

		fig = go.Figure(data=[
			go.Bar(
				y=list(confidence_data.keys()),
				x=list(confidence_data.values()),
				orientation='h',
				marker=dict(
					color=['#28a745' if v >= 70 else '#ffc107' if v >= 40 else '#dc3545' for v in confidence_data.values()]
				),
				text=[f"{v:.1f}%" for v in confidence_data.values()],
				textposition='auto',
			)
		])
		fig.update_layout(
			xaxis_title="Confidence Score (%)",
			yaxis_title="",
			height=300,
			margin=dict(l=0, r=0, t=0, b=0),
			showlegend=False,
			xaxis=dict(range=[0, 100])
		)
		st.plotly_chart(fig, use_container_width=True)

	# Extracted entities
	st.subheader("🏷️ Extracted Entities")

	entity_cols = st.columns(2)

	with entity_cols[0]:
		st.markdown("**Primary Entities:**")
		entity_info = []
		if entities['stakeholder']:
			entity_info.append(f"👤 **Stakeholder:** {entities['stakeholder']}")
		if entities['action']:
			entity_info.append(f"⚙️ **Action:** {entities['action']}")
		if entities['object']:
			entity_info.append(f"📦 **Object:** {entities['object']}")
		if entities['system']:
			entity_info.append(f"🖥️ **System:** {entities['system']}")

		if entity_info:
			st.markdown("\n".join(entity_info))
		else:
			st.info("No primary entities extracted")

	with entity_cols[1]:
		st.markdown("**Secondary Attributes:**")
		attr_info = []
		if entities['priority']:
			attr_info.append(f"🎯 **Priority:** {entities['priority']}")
		if entities['quality']:
			attr_info.append(f"⭐ **Quality Attribute:** {entities['quality']}")
		if entities['conditions']:
			attr_info.append(f"🔄 **Condition:** {entities['conditions']}")
		if entities['constraints']:
			attr_info.append(f"⏱️ **Constraint:** {entities['constraints']}")

		if attr_info:
			st.markdown("\n".join(attr_info))
		else:
			st.info("No secondary attributes extracted")

	# Keywords analysis
	st.subheader("🔑 Keywords Analysis")

	keyword_cols = st.columns(2)

	with keyword_cols[0]:
		if keywords['requirement_keywords']:
			st.markdown("**Requirement Keywords Detected:**")
			keyword_text = ", ".join(f"`{kw}`" for kw in keywords['requirement_keywords'][:10])
			st.markdown(keyword_text)
		else:
			st.info("No requirement keywords detected")

	with keyword_cols[1]:
		if keywords['quality_keywords']:
			st.markdown("**Quality Keywords Detected:**")
			quality_text = ", ".join(f"`{kw}`" for kw in keywords['quality_keywords'][:10])
			st.markdown(quality_text)
		else:
			st.info("No quality keywords detected")

	# Generated Ticket
	st.markdown("---")
	st.subheader("🎫 Generated Business Requirement Ticket")

	# Format ticket for display
	ticket_display = {
		"Ticket ID": ticket['ticket_id'],
		"Title": ticket['title'],
		"Description": ticket['description'],
		"Is Requirement": "✅ Yes" if ticket['is_requirement'] else "❌ No",
		"Requirement Confidence": f"{ticket['requirement_confidence']:.0%}",
		"Stakeholder": ticket['stakeholder'] or "Not specified",
		"Action": ticket['action'] or "Not specified",
		"Object": ticket['object'] or "Not specified",
		"System": ticket['system'] or "Not specified",
		"Priority": ticket['priority'],
		"Quality Attributes": ticket['quality_attributes'] or "Not specified",
		"Conditions": ticket['conditions'] or "None",
		"Constraints": ticket['constraints'] or "None",
		"Status": ticket['status'],
		"Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}

	st.markdown(
		f"""
		<div class="ticket-output">
			{json.dumps(ticket_display, indent=2)}
		</div>
		""",
		unsafe_allow_html=True
	)

	# Export options
	st.markdown("---")
	st.subheader("💾 Export Options")

	export_cols = st.columns(3)

	with export_cols[0]:
		json_str = json.dumps(ticket_display, indent=2)
		st.download_button(
			label="📥 Download as JSON",
			data=json_str,
			file_name=f"{ticket['ticket_id']}.json",
			mime="application/json"
		)

	with export_cols[1]:
		# CSV export
		import csv
		import io
		csv_buffer = io.StringIO()
		writer = csv.writer(csv_buffer)
		for key, value in ticket_display.items():
			writer.writerow([key, value])

		st.download_button(
			label="📋 Download as CSV",
			data=csv_buffer.getvalue(),
			file_name=f"{ticket['ticket_id']}.csv",
			mime="text/csv"
		)

	with export_cols[2]:
		# Full entity data
		entities_json = json.dumps(entities, indent=2)
		st.download_button(
			label="📊 Download Full Analysis",
			data=entities_json,
			file_name=f"{ticket['ticket_id']}_analysis.json",
			mime="application/json"
		)

# Example section
st.markdown("---")
with st.expander("📚 Example Requirements"):
	examples = [
		"We need a mobile application that allows users to track their fitness goals and progress with real-time notifications",
		"Ensure that the new software solution has a user-friendly interface and integrates seamlessly with existing systems",
		"As an administrator, I need the ability to manage user permissions and security roles within the system",
		"The system should support at least 1000 concurrent users with response times under 2 seconds"
	]

	for i, example in enumerate(examples, 1):
		if st.button(f"📌 Example {i}: {example[:50]}...", key=f"example_{i}"):
			st.session_state.user_input = example
			st.rerun()

# Footer
st.markdown("---")
st.markdown(
	"""
	<div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
		Business Requirement Ticket Generator | Powered by SpaCy & Streamlit
	</div>
	""",
	unsafe_allow_html=True
)
