import re
from typing import Dict, Any

class QueryAnalyzer:
    """Analyze user queries to determine routing strategy"""
    
    # Keywords for different query types
    CODE_KEYWORDS = [
        'code', 'function', 'class', 'debug', 'error', 'bug', 'implement',
        'algorithm', 'programming', 'python', 'javascript', 'java', 'c++',
        'sql', 'database', 'api', 'syntax', 'compile', 'runtime'
    ]
    
    CREATIVE_KEYWORDS = [
        'write', 'story', 'poem', 'creative', 'imagine', 'describe',
        'narrative', 'character', 'plot', 'fiction', 'essay', 'article'
    ]
    
    ANALYTICAL_KEYWORDS = [
        'analyze', 'compare', 'evaluate', 'assess', 'research', 'study',
        'investigate', 'examine', 'review', 'critique', 'data', 'statistics'
    ]
    
    @staticmethod
    def analyze(query: str) -> Dict[str, Any]:
        """
        Analyze a query and return metadata
        
        Args:
            query: User's query text
            
        Returns:
            Dictionary with query metadata
        """
        query_lower = query.lower()
        
        # Determine query type
        query_type = QueryAnalyzer._detect_query_type(query_lower)
        
        # Estimate token count (rough estimation)
        token_count = len(query.split())
        
        # Detect complexity
        complexity = QueryAnalyzer._estimate_complexity(query)
        
        # Check for code blocks
        has_code = bool(re.search(r'```|`[^`]+`', query))
        
        return {
            'query_type': query_type,
            'token_count': token_count,
            'complexity': complexity,
            'has_code': has_code,
            'length': len(query),
            'word_count': len(query.split())
        }
    
    @staticmethod
    def _detect_query_type(query_lower: str) -> str:
        """Detect the type of query"""
        code_score = sum(1 for keyword in QueryAnalyzer.CODE_KEYWORDS if keyword in query_lower)
        creative_score = sum(1 for keyword in QueryAnalyzer.CREATIVE_KEYWORDS if keyword in query_lower)
        analytical_score = sum(1 for keyword in QueryAnalyzer.ANALYTICAL_KEYWORDS if keyword in query_lower)
        
        # Check for code patterns
        if re.search(r'```|def |class |function |import |<\w+>', query_lower):
            code_score += 3
        
        scores = {
            'code': code_score,
            'creative': creative_score,
            'analytical': analytical_score
        }
        
        max_score = max(scores.values())
        if max_score == 0:
            return 'general'
        
        return max(scores, key=scores.get)
    
    @staticmethod
    def _estimate_complexity(query: str) -> str:
        """Estimate query complexity"""
        word_count = len(query.split())
        
        if word_count < 20:
            return 'simple'
        elif word_count < 100:
            return 'moderate'
        else:
            return 'complex'
