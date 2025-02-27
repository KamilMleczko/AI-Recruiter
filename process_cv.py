from typing import Dict, Any
from .agents.pdf_summarizer_agent import PdfSummarizerAgent
from .agents.analyzer_agent import AnalyzerAgent
from .agents.job_matcher_agent import JobMatcherAgent
from .agents.evaluator_agent import EvaluatorAgent
from .agents.recommender_agent import RecommenderAgent



async def process_application(cv_data: Dict[str, Any]) -> Dict[str, Any]:
    
    pdf_summarizer = PdfSummarizerAgent()
    analyzer = AnalyzerAgent()
    job_matcher = JobMatcherAgent()
    evaluator = EvaluatorAgent()
    recommender = RecommenderAgent()

    ctx = {
        "resume_data": cv_data,
        "status": "initiated",
        "current_stage": "extraction",
    }

    try:
        structured_text = await pdf_summarizer.run(
            [{"role": "user", "content": str(cv_data)}]
        )
        ctx.update(
            {"extracted_data": structured_text, "current_stage": "analysis"}
        )

        analysis_results = await analyzer.run(
            [{"role": "user", "content": str(structured_text)}]
        )
        ctx.update(
            {"analysis_results": analysis_results, "current_stage": "matching"}
        )

        job_matches = await job_matcher.run(
            [{"role": "user", "content": str(analysis_results)}]
        )
        ctx.update(
            {"job_matches": job_matches, "current_stage": "screening"}
        )

        screening_results = await evaluator.run(
            [{"role": "user", "content": str(ctx)}]
        )
        ctx.update(
            {
                "screening_results": screening_results,
                "current_stage": "recommendation",
            }
        )

        final_recommendation = await recommender.run(
            [{"role": "user", "content": str(ctx)}]
        )
        ctx.update(
            {"final_recommendation": final_recommendation, "status": "completed"}
        )

        return ctx

    except Exception as e:
        ctx.update({"status": "failed", "error": str(e)})
        raise
