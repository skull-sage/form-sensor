"""
Text extraction and parsing utilities for CV analysis.
"""

import re
from typing import List, Dict, Optional, Tuple
from io import BytesIO


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        str: Extracted text
        
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        import PyPDF2
        
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def get_pdf_page_count(file_content: bytes) -> int:
    """
    Get number of pages in PDF.
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        int: Number of pages
    """
    try:
        import PyPDF2
        
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return len(pdf_reader.pages)
    except:
        return 0


def parse_cv_sections(text: str) -> Dict[str, str]:
    """
    Parse CV text and identify all sections in a single pass.
    
    Args:
        text: CV text content
        
    Returns:
        dict: Sections mapped to their content
    """
    lines = text.split('\n')
    sections = {}
    current_section = "header"  # Everything before first section
    current_content = []
    
    # Common section headers
    section_keywords = {
        'experience': ['experience', 'work history', 'employment', 'professional experience', 'work experience'],
        'skills': ['skills', 'technical skills', 'technologies', 'tech stack', 'expertise', 'competencies'],
        'education': ['education', 'academic background', 'qualifications', 'academic'],
        'projects': ['projects', 'personal projects'],
        'certifications': ['certifications', 'certificates', 'licenses'],
        'summary': ['summary', 'profile', 'objective', 'about']
    }
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Check if this line is a section header
        is_section_header = False
        for section_name, keywords in section_keywords.items():
            if any(keyword == line_lower or line_lower.startswith(keyword) for keyword in keywords):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = section_name
                current_content = []
                is_section_header = True
                break
        
        if not is_section_header and line_stripped:
            current_content.append(line_stripped)
    
    # Save last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def extract_basic_info(text: str, sections: Dict[str, str]) -> Dict:
    """
    Extract candidate basic information from CV text.
    
    Args:
        text: CV text content
        sections: Pre-parsed CV sections
        
    Returns:
        dict: Basic info with name, email, phone, address, social_links
    """
    lines = text.split('\n')
    header_text = sections.get('header', '')
    
    return {
        "name": extract_name(lines),
        "email": extract_email(header_text or text),
        "phone": extract_phone(header_text or text),
        "address": extract_address(header_text or text),
        "social_links": extract_social_links(header_text or text)
    }


def extract_name(lines: List[str]) -> Optional[str]:
    """
    Extract candidate name from first few lines of CV.
    Usually the name is in the first 1-3 lines.
    
    Args:
        lines: List of text lines
        
    Returns:
        str: Candidate name or None
    """
    # Look in first 5 lines for a name
    for i, line in enumerate(lines[:5]):
        line = line.strip()
        # Skip empty lines and lines with email/phone
        if not line or '@' in line or re.search(r'\d{3}', line):
            continue
        # Name is usually 2-4 words, all capitalized or title case
        words = line.split()
        if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words if word):
            return line
    
    return None


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text.
    
    Args:
        text: CV text content
        
    Returns:
        str: Email address or None
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text.
    
    Args:
        text: CV text content
        
    Returns:
        str: Phone number or None
    """
    # Various phone patterns
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-234-567-8900
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (234) 567-8900
        r'\+?\d{10,15}'  # +12345678900
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return None


def extract_address(text: str) -> Optional[str]:
    """
    Extract address/location from text.
    Look for city, state, country patterns.
    
    Args:
        text: CV text content
        
    Returns:
        str: Address or None
    """
    # Look for common location patterns
    location_patterns = [
        r'([A-Z][a-z]+,\s*[A-Z]{2})',  # City, ST
        r'([A-Z][a-z]+,\s*[A-Z][a-z]+)',  # City, Country
        r'([A-Z][a-z]+\s*,\s*[A-Z][a-z]+\s*,\s*[A-Z]{2,})'  # City, State, Country
    ]
    
    for pattern in location_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    
    return None


def extract_social_links(text: str) -> Dict[str, str]:
    """
    Extract social media and professional profile links.
    
    Args:
        text: CV text content
        
    Returns:
        dict: Social links by platform
    """
    links = {}
    
    # LinkedIn
    linkedin_pattern = r'(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)'
    linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_matches:
        links['linkedin'] = linkedin_matches[0]
    
    # GitHub
    github_pattern = r'(https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+)'
    github_matches = re.findall(github_pattern, text, re.IGNORECASE)
    if github_matches:
        links['github'] = github_matches[0]
    
    # Portfolio/Website (generic)
    portfolio_pattern = r'(https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)'
    portfolio_matches = re.findall(portfolio_pattern, text)
    # Filter out linkedin and github
    for match in portfolio_matches:
        if 'linkedin' not in match.lower() and 'github' not in match.lower():
            links['portfolio'] = match
            break
    
    return links


def extract_work_experience(sections: Dict[str, str]) -> List[Dict]:
    """
    Extract work experience from CV sections.
    
    Args:
        sections: Pre-parsed CV sections
        
    Returns:
        list: List of work experience entries
    """
    experiences = []
    
    # Get experience section
    experience_section = sections.get('experience', '')
    
    if not experience_section:
        return experiences
    
    # Split into individual job entries (simplified approach)
    # Look for date patterns as job separators
    date_pattern = r'(\d{4}\s*[-–]\s*(?:\d{4}|Present|Current))'
    
    # This is a simplified extraction - in production, you'd want more sophisticated parsing
    lines = experience_section.split('\n')
    current_job = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line contains a date range
        date_match = re.search(date_pattern, line, re.IGNORECASE)
        if date_match:
            if current_job:
                experiences.append(current_job)
            
            dates = parse_date_range(date_match.group(1))
            current_job = {
                "company": extract_company_from_line(line),
                "start_date": dates[0],
                "end_date": dates[1],
                "description": ""
            }
        elif current_job:
            # Add to description
            current_job["description"] += line + " "
    
    if current_job:
        experiences.append(current_job)
    
    return experiences


def extract_skill_keywords(sections: Dict[str, str]) -> List[str]:
    """
    Extract skill keywords from CV sections.
    Generic approach - extracts whatever is listed in skills section.
    
    Args:
        sections: Pre-parsed CV sections
        
    Returns:
        list: List of unique skill keywords
    """
    skills = set()
    
    # Get skills section
    skills_section = sections.get('skills', '')
    
    if not skills_section:
        return []
    
    # Split by common delimiters
    # Skills are often listed as: "Python, JavaScript, React" or "Python | JavaScript | React" or bullet points
    delimiters = [',', '|', '•', '·', '-', '\n']
    
    # Replace all delimiters with a common one
    normalized_text = skills_section
    for delimiter in delimiters[1:]:  # Keep comma, replace others
        normalized_text = normalized_text.replace(delimiter, ',')
    
    # Split by comma and clean up
    skill_items = normalized_text.split(',')
    
    for item in skill_items:
        skill = item.strip()
        # Filter out empty strings and very long items (likely not skills)
        if skill and len(skill) > 1 and len(skill) < 50:
            # Remove common prefixes like "- " or "• "
            skill = re.sub(r'^[-•·\s]+', '', skill)
            # Remove trailing punctuation
            skill = skill.rstrip('.,;:')
            
            if skill:
                skills.add(skill)
    
    return sorted(list(skills))


def extract_education(sections: Dict[str, str]) -> List[Dict]:
    """
    Extract education qualifications from CV sections.
    
    Args:
        sections: Pre-parsed CV sections
        
    Returns:
        list: List of education entries
    """
    education_list = []
    
    # Get education section
    education_section = sections.get('education', '')
    
    if not education_section:
        return education_list
    
    # Look for degree patterns
    degree_patterns = [
        r"(Bachelor(?:'s)?|BS|BA|B\.S\.|B\.A\.)\s+(?:of\s+)?(?:Science|Arts)?\s+in\s+([^,\n]+)",
        r"(Master(?:'s)?|MS|MA|M\.S\.|M\.A\.)\s+(?:of\s+)?(?:Science|Arts)?\s+in\s+([^,\n]+)",
        r"(PhD|Ph\.D\.|Doctorate)\s+in\s+([^,\n]+)",
        r"(MBA|M\.B\.A\.)",
        r"(Diploma|Certificate)\s+in\s+([^,\n]+)"
    ]
    
    lines = education_section.split('\n')
    current_edu = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for degree
        for pattern in degree_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                if current_edu:
                    education_list.append(current_edu)
                
                degree = match.group(0)
                current_edu = {
                    "degree": degree,
                    "institution": "",
                    "graduation_date": None
                }
                break
        
        # Look for institution (usually contains "University", "College", "Institute")
        if current_edu and not current_edu["institution"]:
            if any(word in line for word in ['University', 'College', 'Institute', 'School']):
                current_edu["institution"] = line
        
        # Look for graduation date
        if current_edu and not current_edu["graduation_date"]:
            date_match = re.search(r'(\d{4})', line)
            if date_match:
                current_edu["graduation_date"] = date_match.group(1)
    
    if current_edu:
        education_list.append(current_edu)
    
    return education_list


# Helper functions

def parse_date_range(date_str: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse date range string into start and end dates.
    
    Args:
        date_str: Date range string (e.g., "2020 - 2023", "Jan 2020 - Present")
        
    Returns:
        tuple: (start_date, end_date) in ISO format or "Present"
    """
    date_str = date_str.strip()
    
    # Split by dash or hyphen
    parts = re.split(r'\s*[-–]\s*', date_str)
    
    if len(parts) != 2:
        return (None, None)
    
    start = parts[0].strip()
    end = parts[1].strip()
    
    # Check for "Present" or "Current"
    if re.search(r'present|current', end, re.IGNORECASE):
        end = "Present"
    
    # Try to extract year
    start_year = re.search(r'\d{4}', start)
    end_year = re.search(r'\d{4}', end) if end != "Present" else None
    
    start_date = start_year.group(0) if start_year else None
    end_date = end_year.group(0) if end_year else end
    
    return (start_date, end_date)


def extract_company_from_line(line: str) -> str:
    """
    Extract company name from a line containing job info.
    
    Args:
        line: Line of text
        
    Returns:
        str: Company name
    """
    # Remove date patterns
    line = re.sub(r'\d{4}\s*[-–]\s*(?:\d{4}|Present|Current)', '', line, flags=re.IGNORECASE)
    # Remove common job titles
    line = re.sub(r'(Senior|Junior|Lead|Principal|Staff)?\s*(Software|Web|Full[- ]?Stack|Backend|Frontend|Data|DevOps)?\s*(Engineer|Developer|Architect|Analyst)', '', line, flags=re.IGNORECASE)
    
    return line.strip()
