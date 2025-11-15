import json
import uuid

from sqlite_core.connection_factory import ConnectionFactory


class ScenarioResultsService:

    @classmethod
    def insert(cls, scenario: str,step:str, payload:str)->str:
        id = str(uuid.uuid4())
        with ConnectionFactory.create_connection() as cx:
            cx.execute("""
                INSERT INTO scenario_results (id, scenario, step, payload)
                VALUES (?, ?, ?, ?)
            """, (id, scenario, step, payload))
        return id

    @classmethod
    def get_results_by_scenario(cls,scenario: str):
        with ConnectionFactory.create_connection() as cx:
            cursor = cx.execute("""
                SELECT payload
                FROM scenario_results
                WHERE scenario = ?
            """, (scenario,))
            rows = cursor.fetchall()
            return [json.loads(row[0]) for row in rows if row[0]]

    @classmethod
    def delete_by_scenario(cls, scenario: str)->int:
        with ConnectionFactory.create_connection() as cx:
            result = cx.execute("""
                DELETE FROM scenario_results
                WHERE scenario = ?
            """, (scenario,))
            return result.rowcount
