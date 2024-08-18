from create_strategy_tables_tensor import build_a_strategy_table_tensor,generate_strategy_for_all_true_counts
from simulation import multi_process_multi_player_simulation
import json




def simulate_strategy():
    
    try:
        with open('simulation_configuration.json', 'r') as config_file:
            config = json.load(config_file)
        multi_process_multi_player_simulation(**config)
    except FileNotFoundError:
        raise Exception("Configuration file not found. Ensure 'simulation_configuration.json' is present.")
    except json.JSONDecodeError:
        raise Exception("Error decoding 'simulation_configuration.json'. Check for proper JSON formatting.")



def build_strategy_from_config():
    try:
        with open('create_strategy_configuration.json', 'r') as config_file:
            config = json.load(config_file)
        build_a_strategy_table_tensor(**config)
    except FileNotFoundError:
        raise Exception("Configuration file not found. Ensure 'create_strategy_configuration.json' is present.")
    except json.JSONDecodeError:
        raise Exception("Error decoding 'create_strategy_configuration.json'. Check for proper JSON formatting.")
    except KeyError as e:
        raise Exception(f"Missing necessary configuration parameter: {e}")


def build_full_strategy(repetitions = 1000):
    generate_strategy_for_all_true_counts(repetitions=repetitions)




if __name__ == "__main__":
    print('start')
    # simulate_strategy()
    # build_strategy_fro(m_config()
    #build_full_strategy()