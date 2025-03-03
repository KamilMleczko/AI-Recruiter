from typing import Dict, Any
from .agents.pdf_summarizer_agent import PdfSummarizerAgent
from .agents.analyzer_agent import AnalyzerAgent
from .agents.job_matcher import JobMatcher
from .agents.evaluator_agent import EvaluatorAgent
from .agents.recommender_agent import RecommenderAgent
from app_config import max_job_matches_num


async def process_application(cv_data: Dict[str, Any]) -> Dict[str, Any]:
    
    pdf_summarizer = PdfSummarizerAgent()
    analyzer = AnalyzerAgent()
    job_matcher = JobMatcher() #not an agent but works alongside them
    evaluator = EvaluatorAgent()
    recommender = RecommenderAgent()

    ctx = {
        "cv_data": cv_data,
        "current_stage": "pdf summarization",
    }

    try:
        summarizer_output = await pdf_summarizer.run(
            [{"role": "user", "content": str(cv_data)}]
        )
        ctx.update(
            {"summarizer_output": summarizer_output, "current_stage": "analysis"}
        )

        analysis_results = await analyzer.run(
            [{"role": "user", "content": str(summarizer_output)}]
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

        candidate_to_jobs_evaluation =[]
        for i in range(max_job_matches_num):
            evaluator_results = await evaluator.run(
                [{"role": "user", "content": str(ctx)}], i
            )
            candidate_to_jobs_evaluation.append(evaluator_results)

        ctx.update(
            {
                "candidate_to_jobs_evaluation": candidate_to_jobs_evaluation,
                "current_stage": "recommendation",
            }
        )

        final_recommendation = await recommender.run(
            [{"role": "user", "content": str(ctx)}]
        )
        ctx.update(
            {"final_recommendation": final_recommendation}
        )

        return ctx

    except Exception as e:
        ctx.update({"status": "failed", "error": str(e)})
        raise
