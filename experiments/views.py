from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from langchain_community.utilities import SQLDatabase
import os
from anthropic import Anthropic


class LLMAnalysisViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"])
    def analyze(self, request):
        question = request.data.get("question")
        if not question:
            return Response({"error": "질문을 입력해주세요."}, status=400)

        try:
            # DB 연결 설정은 동일...
            db_settings = settings.DATABASES["default"]
            db_url = (
                f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}@"
                f"{db_settings.get('HOST', 'localhost')}:{db_settings.get('PORT', '5432')}/"
                f"{db_settings['NAME']}"
            )
            db = SQLDatabase.from_uri(db_url)

            # Anthropic 클라이언트 초기화
            anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            # SQL 쿼리 생성을 위한 메시지
            sql_response = anthropic.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=1024,
                system="""You are a PostgreSQL query generator. Generate ONLY SQL queries.
                STRICT RULES:
                1. Return ONLY the SQL query, nothing else
                2. Query MUST start with SELECT
                3. NO explanations, NO comments
                4. NO Korean text except in LIKE conditions
                5. Use proper table aliases (u for users, d for departments, t for tasks)
                6. Always include proper JOIN conditions
                7. When counting employees in headquarters, include both:
                - Direct headquarters members (department_id = headquarters.id)
                - Team members (department_id = team.id where team.parent_id = headquarters.id)

                Database Schema:
                organizations_department (d):
                id, name, code, parent_id
                - parent_id NULL means headquarters (본부)
                - parent_id NOT NULL means team under headquarters (팀)

                accounts_user (u):
                id, department_id, username, first_name, last_name, role, rank, is_active
                - department_id references organizations_department(id)
                - is_active default true

                tasks_task (t):
                id, assignee_id, department_id, title, status, priority, difficulty
                - assignee_id references accounts_user(id)
                - department_id references organizations_department(id)
                - status: TODO/IN_PROGRESS/REVIEW/DONE/HOLD

                tasks_taskevaluation (te):
                id, task_id, evaluator_id, performance_score
                - task_id references tasks_task(id)
                - evaluator_id references accounts_user(id)
                - performance_score: 1-5

                Example Queries:

                1. Count employees in 백엔드팀:
                SELECT COUNT(*) FROM accounts_user u 
                JOIN organizations_department d ON u.department_id = d.id 
                WHERE d.name LIKE '%백엔드%' AND u.is_active = true;

               2. List all teams and employee counts in 푸드테크본부:
            SELECT 
                (SELECT STRING_AGG(dept_info, ', ')
                FROM (
                    SELECT 
                        CASE 
                            WHEN d.parent_id IS NULL THEN d.name || ' 직속 ' || COUNT(DISTINCT u.id) || '명'
                            ELSE d.name || ' ' || COUNT(DISTINCT u.id) || '명'
                        END as dept_info
                    FROM organizations_department p
                    LEFT JOIN organizations_department d ON d.id = p.id OR d.parent_id = p.id
                    LEFT JOIN accounts_user u ON u.department_id = d.id AND u.is_active = true
                    WHERE p.name LIKE '%푸드테크%' AND p.parent_id IS NULL
                    GROUP BY d.id, d.name, d.parent_id
                    ORDER BY d.parent_id NULLS FIRST, d.name
                ) subq
                ) as breakdown,
                (SELECT COUNT(DISTINCT u.id)
                FROM organizations_department p
                LEFT JOIN organizations_department d ON d.id = p.id OR d.parent_id = p.id
                LEFT JOIN accounts_user u ON u.department_id = d.id AND u.is_active = true
                WHERE p.name LIKE '%푸드테크%' AND p.parent_id IS NULL
                ) as total_count;

                3. Find best performing employee:
                SELECT u.last_name || u.first_name as name, d.name as dept, 
                    ROUND(AVG(te.performance_score)::numeric, 1) as score
                FROM accounts_user u 
                JOIN tasks_task t ON t.assignee_id = u.id 
                JOIN tasks_taskevaluation te ON te.task_id = t.id 
                JOIN organizations_department d ON u.department_id = d.id 
                WHERE t.status = 'DONE' 
                GROUP BY u.id, u.last_name, u.first_name, d.name 
                HAVING COUNT(te.id) >= 3 
                ORDER BY score DESC LIMIT 1;

                REMEMBER: Return ONLY the SQL query. Any other text will cause an error.""",  # 기존 system_prompt 내용
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate a PostgreSQL query to answer: {question}"
                    }
                ]
            )

            sql_query = sql_response.content[0].text

            # 쿼리 검증 로직은 동일...
            if (
                not sql_query.strip().upper().startswith("SELECT")
                or "이" in sql_query
                or "를" in sql_query
            ):
                return Response(
                    {
                        "error": "유효한 쿼리를 생성할 수 없습니다.",
                        "sql_query": "SELECT NULL AS error;",
                        "result": None,
                    },
                    status=400,
                )

            # 쿼리 실행
            result = db.run(sql_query)

            # 결과 포맷팅을 위한 메시지
            format_response = anthropic.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=1024,
                system="""You are a helpful assistant that formats database query results into natural Korean sentences...""",  # 기존 format_prompt 내용
                messages=[
                    {
                        "role": "user",
                        "content": f"Question: {question}\nSQL: {sql_query}\nResult: {result}"
                    }
                ]
            )

            formatted_result = format_response.content[0].text

            return Response(
                {
                    "question": question,
                    "sql_query": sql_query,
                    "result": result,
                    "formatted_result": formatted_result,
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
