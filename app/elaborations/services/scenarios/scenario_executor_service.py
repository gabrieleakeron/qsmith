from elaborations.services.scenarios.scenario_executor_thread import ScenarioExecutorThread

def execute_scenario_by_id(scenario_id: str):
    ScenarioExecutorThread(scenario_id).start()
