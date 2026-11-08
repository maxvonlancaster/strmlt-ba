"""
Requirement Processing Pipeline
Handles text vectorization, entity extraction, and requirement analysis
"""

import re
from typing import Dict, List, Tuple, Optional
import spacy
from spacy.pipeline import EntityRuler


# Spacy model and patterns configuration
ENTITIES = [
	"STAKEHOLDER",
	"SYSTEM",
	"ACTION",
	"OBJECT",
	"CONDITION",
	"CONSTRAINT",
	"PRIORITY",
	"QUALITY"
]

STAKEHOLDER_MAP = {
	"we": "organization",
	"our": "organization",
	"our team": "organization",
	"the company": "organization",
	"company": "organization",
	"customer": "customer",
	"clients": "customer",
	"client": "customer",
	"user": "user",
	"users": "user",
	"admin": "administrator",
	"administrator": "administrator",
	"manager": "manager",
	"developer": "developer",
	"developers": "developer",
	"stakeholder": "stakeholder",
	"end-user": "user",
	"end user": "user",
	"system admin": "administrator",
}

# Requirement keywords that indicate a business requirement
REQUIREMENT_KEYWORDS = {
	"need", "needs", "needed", "require", "requires", "required", "requirement",
	"must", "should", "shall", "will", "have to", "has to",
	"ensure", "maintain", "support", "allow", "enable", "provide",
	"implement", "build", "create", "develop", "design", "add", "integrate"
}

# Quality/Non-functional requirement keywords
QUALITY_KEYWORDS = {
	"secure", "security", "scalable", "scalability", "reliable", "reliability",
	"fast", "speed", "efficient", "efficiency", "user-friendly", "usable",
	"robust", "maintainable", "maintainability", "portable", "portability",
	"available", "availability", "responsive", "responsive", "performant",
	"performance", "interoperable", "compatible"
}

# Priority keywords
PRIORITY_KEYWORDS = {
	"high": "high",
	"critical": "high",
	"urgent": "high",
	"medium": "medium",
	"normal": "medium",
	"low": "low",
	"minor": "low"
}


class RequirementProcessor:
	"""Process unstructured text to extract business requirements"""

	def __init__(self):
		"""Initialize the requirement processor with spaCy model and patterns"""
		self.nlp = self._load_spacy_model()

		# Remove existing entity_ruler if present
		if "entity_ruler" in self.nlp.pipe_names:
			self.nlp.remove_pipe("entity_ruler")

		# Add entity ruler with patterns
		self._add_entity_patterns()

	def _load_spacy_model(self):
		"""Load spaCy model with multiple fallback strategies"""
		import subprocess
		import sys

		# Try to load the model
		try:
			return spacy.load("en_core_web_sm")
		except OSError:
			pass

		# If not found, try to download it using subprocess
		try:
			print("Downloading spaCy model 'en_core_web_sm'...")
			subprocess.check_call(
				[sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
				stdout=subprocess.DEVNULL,
				stderr=subprocess.DEVNULL
			)
			return spacy.load("en_core_web_sm")
		except Exception as e:
			print(f"Warning: Could not download model: {e}")
			print("Attempting to use blank English model instead...")

		# Fallback to blank English model if download fails
		try:
			return spacy.blank("en")
		except Exception as e:
			raise RuntimeError(
				f"Failed to load or create spaCy model. Error: {e}\n"
				"Please try running locally: python -m spacy download en_core_web_sm"
			)

	def _add_entity_patterns(self):
		"""Add spaCy entity ruler patterns for requirement extraction"""
		# Check if we have a tagger for POS-based patterns
		has_tagger = "tagger" in self.nlp.pipe_names or "morphologizer" in self.nlp.pipe_names

		patterns = [
			# STAKEHOLDER: expanded list and phrases
			{"label": "STAKEHOLDER", "pattern": [{"LOWER": {"IN": ["user", "admin", "administrator", "manager", "client", "customer", "organization", "we", "our", "the company", "developer", "stakeholder", "end-user", "end user", "system admin"]}}]},
			{"label": "STAKEHOLDER", "pattern": [{"LOWER": "the"}, {"LOWER": {"IN": ["user", "admin", "client", "customer", "company"]}}]},
			{"label": "STAKEHOLDER", "pattern": [{"LOWER": {"IN": ["system", "application", "platform", "software"]}}]},

			# SYSTEM: expanded
			{"label": "SYSTEM", "pattern": [{"LOWER": {"IN": ["system", "platform", "application", "software", "service", "module", "component", "app"]}}]},
			{"label": "SYSTEM", "pattern": [{"LOWER": "the"}, {"LOWER": {"IN": ["system", "application", "platform", "app"]}}]},

			# ACTION: modal verbs and common requirement verbs (without POS for blank models)
			{"label": "ACTION", "pattern": [{"LOWER": {"IN": ["shall", "must", "should", "will"]}}]},
		]

		# Only add POS-dependent patterns if tagger is available
		if has_tagger:
			patterns.extend([
				{"label": "ACTION", "pattern": [{"POS": "VERB", "LEMMA": {"IN": ["generate", "export", "validate", "allow", "provide", "support", "handle", "process", "create", "update", "delete", "send", "receive", "display", "store", "retrieve", "authenticate", "authorize", "manage", "track", "schedule", "browse", "purchase", "integrate"]}}]},

				# OBJECT: software-related nouns
				{"label": "OBJECT", "pattern": [{"POS": "NOUN", "LEMMA": {"IN": ["report", "data", "file", "user", "password", "account", "session", "email", "notification", "dashboard", "interface", "database", "api", "request", "response", "order", "payment", "booking", "delivery", "tracking"]}}]},

				# CONDITION: when/if/after clauses
				{"label": "CONDITION", "pattern": [{"LOWER": {"IN": ["when", "if", "after", "before", "while"]}}, {"POS": "DET", "OP": "?"}, {"POS": "NOUN"}]},
				{"label": "CONDITION", "pattern": [{"LOWER": "upon"}, {"POS": "VERB"}]},

				# CONSTRAINT: time and quantity constraints
				{"label": "CONSTRAINT", "pattern": [{"LOWER": {"IN": ["within", "less", "than", "no more", "at least", "maximum", "minimum"]}}, {"POS": "NUM"}, {"LOWER": {"IN": ["seconds", "minutes", "hours", "days", "ms", "milliseconds"]}}]},
				{"label": "CONSTRAINT", "pattern": [{"POS": "NUM"}, {"LOWER": {"IN": ["seconds", "minutes", "hours", "days", "ms", "milliseconds"]}}]},
			])
		else:
			# Fallback patterns for blank model without POS tags
			patterns.extend([
				# OBJECT: common object keywords
				{"label": "OBJECT", "pattern": [{"LOWER": {"IN": ["report", "data", "file", "user", "password", "account", "session", "email", "notification", "dashboard", "interface", "database", "api", "request", "response", "order", "payment", "booking", "delivery", "tracking"]}}]},

				# CONDITION: when/if/after clauses
				{"label": "CONDITION", "pattern": [{"LOWER": {"IN": ["when", "if", "after", "before", "while"]}}]},
				{"label": "CONDITION", "pattern": [{"LOWER": "upon"}]},

				# CONSTRAINT: time and quantity constraints
				{"label": "CONSTRAINT", "pattern": [{"LOWER": {"IN": ["within", "less", "than", "no more", "at least", "maximum", "minimum"]}}]},
			])

		patterns.extend([
			# PRIORITY
			{"label": "PRIORITY", "pattern": [{"LOWER": {"IN": ["high", "medium", "low", "critical", "urgent"]}}]},

			# QUALITY: Non-functional requirements
			{"label": "QUALITY", "pattern": [{"LOWER": {"IN": ["secure", "scalable", "reliable", "fast", "efficient", "user-friendly", "robust", "maintainable", "portable", "available", "responsive", "performant", "interoperable", "compatible"]}}]},
		])

		# Only add entity_ruler before "ner" if "ner" component exists
		if "ner" in self.nlp.pipe_names:
			ruler = self.nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})
		else:
			ruler = self.nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
		ruler.add_patterns(patterns)

	def _extract_dependency_structure(self, doc, result: Dict) -> Dict:
		"""Enrich entity extraction using syntactic dependencies"""
		# Find ROOT verb (main action)
		root = None
		for token in doc:
			if token.dep_ == "ROOT" and token.pos_ == "VERB":
				root = token
				break

		if root:
			# Prefer xcomp (more specific action)
			for child in root.children:
				if child.dep_ == "xcomp" and child.pos_ == "VERB":
					result["action"] = child.lemma_
					break
			else:
				result["action"] = root.lemma_

		# Find stakeholder (subject)
		for token in doc:
			if token.dep_ in ["nsubj", "nsubjpass"]:
				subj = token.text.lower()
				result["stakeholder"] = STAKEHOLDER_MAP.get(subj, token.text)

		# Find object (what is acted upon)
		for token in doc:
			if token.dep_ in ["dobj", "pobj", "attr"]:
				result["object"] = token.text

		# Extract conditions (when/if clauses)
		for token in doc:
			if token.dep_ in ["advcl", "mark"] and token.text.lower() in ["when", "if", "after", "before"]:
				condition_span = " ".join([t.text for t in token.subtree])
				result["conditions"] = condition_span

		# Extract constraints (numbers, timing)
		for token in doc:
			if token.like_num:
				span = " ".join([t.text for t in token.subtree])
				result["constraints"] = span

		return result

	def extract_entities(self, text: str) -> Dict:
		"""Extract structured entities from requirement text"""
		doc = self.nlp(text)

		result = {
			"stakeholder": None,
			"system": None,
			"action": None,
			"object": None,
			"conditions": None,
			"constraints": None,
			"priority": None,
			"quality": None,
			"confidence": 0.0,
			"originalText": text
		}

		entities_found = 0

		# Extract entities from spaCy NER
		for ent in doc.ents:
			entities_found += 1
			if ent.label_ == "STAKEHOLDER":
				if ent.text.lower() in STAKEHOLDER_MAP:
					result["stakeholder"] = STAKEHOLDER_MAP[ent.text.lower()]
				else:
					result["stakeholder"] = ent.text
			elif ent.label_ == "SYSTEM":
				result["system"] = ent.text
			elif ent.label_ == "ACTION":
				result["action"] = ent.text
			elif ent.label_ == "OBJECT":
				result["object"] = ent.text
			elif ent.label_ == "CONDITION":
				result["conditions"] = ent.text
			elif ent.label_ == "CONSTRAINT":
				result["constraints"] = ent.text
			elif ent.label_ == "PRIORITY":
				priority_lower = ent.text.lower()
				result["priority"] = PRIORITY_KEYWORDS.get(priority_lower, ent.text)
			elif ent.label_ == "QUALITY":
				result["quality"] = ent.text

		# Enrich with dependency parsing
		result = self._extract_dependency_structure(doc, result)

		# Calculate confidence based on entity presence
		base_confidence = min(entities_found / 5.0, 1.0)

		# Boost if key entities present
		if result["stakeholder"] and result["action"] and result["object"]:
			base_confidence = min(base_confidence + 0.3, 1.0)

		result["confidence"] = round(base_confidence, 2)

		return result

	def extract_keywords(self, text: str) -> Dict[str, List[str]]:
		"""Extract requirement-related keywords from text"""
		text_lower = text.lower()
		doc = self.nlp(text)

		keywords = {
			"requirement_keywords": [],
			"quality_keywords": [],
			"entities": {}
		}

		# Extract requirement keywords
		words = text_lower.split()
		for word in words:
			clean_word = re.sub(r'[^\w]', '', word)
			if clean_word in REQUIREMENT_KEYWORDS:
				keywords["requirement_keywords"].append(word)
			elif clean_word in QUALITY_KEYWORDS:
				keywords["quality_keywords"].append(word)

		# Extract entity positions for highlighting
		for ent in doc.ents:
			if ent.label_ in ENTITIES:
				if ent.label_ not in keywords["entities"]:
					keywords["entities"][ent.label_] = []
				keywords["entities"][ent.label_].append({
					"text": ent.text,
					"start": ent.start_char,
					"end": ent.end_char
				})

		return keywords

	def highlight_text(self, text: str) -> List[Tuple[str, str]]:
		"""
		Create highlighted text with entity markers
		Returns list of (text, label) tuples for rendering
		"""
		doc = self.nlp(text)

		# Build entity map with positions
		entity_map = {}
		for ent in doc.ents:
			entity_map[(ent.start_char, ent.end_char)] = ent.label_

		# Sort entities by start position
		sorted_entities = sorted(entity_map.keys())

		highlighted = []
		last_end = 0

		for start, end in sorted_entities:
			# Add text before entity
			if start > last_end:
				highlighted.append((text[last_end:start], "normal"))

			# Add entity with label
			label = entity_map[(start, end)]
			highlighted.append((text[start:end], label))
			last_end = end

		# Add remaining text
		if last_end < len(text):
			highlighted.append((text[last_end:], "normal"))

		return highlighted

	def is_requirement(self, text: str, confidence_threshold: float = 0.5) -> Tuple[bool, float]:
		"""
		Determine if text is a business requirement
		Uses heuristic based on requirement keywords and entity presence
		"""
		entities = self.extract_entities(text)
		keywords = self.extract_keywords(text)

		# Scoring heuristic
		score = 0.0

		# Check for requirement keywords (high weight)
		if keywords["requirement_keywords"]:
			score += 0.4

		# Check for stakeholder and action (high weight)
		if entities["stakeholder"] and entities["action"]:
			score += 0.3

		# Check for object
		if entities["object"]:
			score += 0.15

		# Check for quality attributes (medium weight)
		if keywords["quality_keywords"] or entities["quality"]:
			score += 0.15

		# Use entity confidence
		score = max(score, entities["confidence"])

		return score >= confidence_threshold, round(score, 2)


def create_ticket(entities: Dict, is_requirement: bool, requirement_score: float) -> Dict:
	"""
	Create a business requirement ticket from extracted entities
	"""
	action = entities.get('action') or 'Unknown'
	object_name = entities.get('object') or 'requirement'

	ticket = {
		"ticket_id": "REQ-" + str(hash(entities["originalText"]))[-8:].upper(),
		"is_requirement": is_requirement,
		"requirement_confidence": requirement_score,
		"title": f"{action.upper()} - {object_name}",
		"description": entities["originalText"],
		"stakeholder": entities.get("stakeholder"),
		"system": entities.get("system"),
		"action": entities.get("action"),
		"object": entities.get("object"),
		"conditions": entities.get("conditions"),
		"constraints": entities.get("constraints"),
		"priority": entities.get("priority") or "medium",
		"quality_attributes": entities.get("quality"),
		"extraction_confidence": entities.get("confidence", 0.0),
		"status": "extracted"
	}

	return ticket
