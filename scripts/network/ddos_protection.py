import time

# limit = how many commands the user can send in 1 minute
# failed_limit = how many commands that we fail to execute can user send in 1 minute
COMMAND_SEND_LIMITS_BY_COMMAND_NAME = {
    "system;init_location;":{"limit":2, "failed_limit":2},
    "system;c01;":{"limit":5, "failed_limit":5},
    "system;get_aes_data":{"limit":2, "failed_limit":2},
    "battle;ping":{"limit":60, "failed_limit":10},
    "garage;get_garage_data":{"limit":5, "failed_limit":2},
    "battle;check_md5_map":{"limit":3, "failed_limit":2},
    "lobby;user_inited":{"limit":2, "failed_limit":3},
    "lobby;try_create_battle_dom":{"limit":7, "failed_limit":7},
    "lobby;try_create_battle_ctf":{"limit":7, "failed_limit":7},
    "lobby;try_create_battle_tdm":{"limit":7, "failed_limit":7},
    "lobby;try_create_battle_dm":{"limit":7, "failed_limit":7},
    "lobby;get_show_battle_info":{"limit":15, "failed_limit":15},
    "lobby;enter_battle":{"limit":3, "failed_limit":2},
    "lobby;enter_battle_team":{"limit":3, "failed_limit":2},
    "lobby;check_battleName_for_forbidden_words":{"limit":50, "failed_limit":4},
    "lobby;enter_battle_spectator":{"limit":3, "failed_limit":2},
    "lobby_chat;message":{"limit":12, "failed_limit":5},
    "garage;try_mount_item":{"limit":10, "failed_limit":3},
    "garage;try_buy_item":{"limit":12, "failed_limit":3},
    "garage;try_update_item":{"limit":12, "failed_limit":3},
    "auth;confirm_email_code":{"limit":5, "failed_limit":3},
    "auth;recovery_account":{"limit":5, "failed_limit":3},
    "auth;change_pass_email":{"limit":5, "failed_limit":3},
    "lobby;change_quest":{"limit":5, "failed_limit":2},
    "lobby;generate_key_email":{"limit":5, "failed_limit":0},
    "lobby;confirm_email_code_recovery":{"limit":4, "failed_limit":0},
    "lobby;change_password":{"limit":4, "failed_limit":0},
    "lobby;update_profile":{"limit":4, "failed_limit":0},
    "lobby;screenshot":{"limit":3, "failed_limit":0},
    "lobby;bug_report":{"limit":3, "failed_limit":0},
    "battle;attempt_to_take_bonus":{"limit":10, "failed_limit":0},
    "battle;get_init_data_local_tank":{"limit":4, "failed_limit":0},
    "battle;spectator_user_init":{"limit":4, "failed_limit":0},
    "battle;speedhack_detected":{"limit":7, "failed_limit":0},
    "battle;exit_from_statistic":{"limit":4, "failed_limit":0},
    "battle;activate_graffiti":{"limit":5, "failed_limit":0},
    "battle;chat":{"limit":10, "failed_limit":0},
    "battle;activate_item":{"limit":12, "failed_limit":0},
    "battle;mine_hit":{"limit":50, "failed_limit":0},
    "battle;attempt_to_take_flag":{"limit":5, "failed_limit":0},
    "battle;flag_drop":{"limit":5, "failed_limit":0},
    "battle;tank_capturing_point":{"limit":15, "failed_limit":0},
    "battle;tank_leave_capturing_point":{"limit":15, "failed_limit":0},
    "battle;activate_tank":{"limit":12, "failed_limit":0},
    "battle;move":{"limit":70, "failed_limit":0},
    "battle;suicide":{"limit":11, "failed_limit":0},
    "battle;start_fire":{"limit":60, "failed_limit":0},
    "battle;stop_fire":{"limit":60, "failed_limit":0},
    "battle;fire":{"limit":60, "failed_limit":0},
    "battle;quick_shot_shaft":{"limit":30, "failed_limit":0},
    "battle;begin_enegry_drain":{"limit":50, "failed_limit":0},
    "auth;refresh_captcha":{"limit":11, "failed_limit":0},
    "lobby;deny_friend":{"limit":60, "failed_limit":0},
    "lobby;make_friend":{"limit":60, "failed_limit":0},
    "lobby;accept_friend":{"limit":50, "failed_limit":0},
    "lobby;cancel_request":{"limit":30, "failed_limit":0}
}

class CommandSendCount:
    def __init__(self):
        self.send_count = 0
        self.time = time.time()

    def count_command(self, ip, command_name, failed):
        self.send_count += 1
        time_from_last_check = time.time() - self.time

        if time_from_last_check >= server_properties.DDOS_COMMAND_COUNTER_RESET_TIME:
            self.send_count = 0
            self.time = time.time()

        if failed:
            command_limit = COMMAND_SEND_LIMIT_BY_COMMAND_NAME[command_name]["failed_limit"]
        else:
            command_limit = COMMAND_SEND_LIMIT_BY_COMMAND_NAME[command_name]["limit"]

        if self.send_count / (self.time / 60) >= command_limit:
            logging.info("DDOS protection banned user with ip: " + ip)
            # TODO: ban the ip

class CommandCounter:
    def __init__(self):
        self.command_send_counts_by_ip = {} # {"127.0.0.1":{"chat":<CommandSendCount>}}

    def command_exist_check(self, ip, command_name):
        if not ip in self.command_send_counts_by_ip:
            self.command_send_counts_by_ip[ip] = {}

        if not command_name in self.command_send_counts_by_ip[ip]:
            self.command_send_counts_by_ip[ip][command_name] = CommandSendCount()

    def count_command(self, ip, command_buffer, failed=False):
        command_name = command_buffer.get_argument_with_index(0) + ";" + command_buffer.get_argument_with_index(1)
        self.command_exist_check(ip, command_buffer)

        command_send_count = self.command_send_counts_by_ip[ip][command_name] = CommandSendCount()
        command_send_count.count_command(ip, command_name, failed)

command_counter = CommandCounter()
