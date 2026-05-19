from unittest.mock import MagicMock, patch
from poller import Poller


def _make_player(name, is_dead, riot_id=None):
    return {
        "summonerName": name,
        "riotIdGameName": riot_id or "",
        "isDead": is_dead,
    }


def _make_poller(**kwargs):
    defaults = dict(on_death=MagicMock(), on_respawn=MagicMock())
    defaults.update(kwargs)
    return Poller(**defaults)


def test_on_death_fires_on_alive_to_dead_transition():
    p = _make_poller()
    p._in_game = True
    p._was_dead = False

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", True)]):
        p._tick()

    p.on_death.assert_called_once()
    p.on_respawn.assert_not_called()


def test_on_respawn_fires_on_dead_to_alive_transition():
    p = _make_poller()
    p._in_game = True
    p._was_dead = True

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    p.on_respawn.assert_called_once()
    p.on_death.assert_not_called()


def test_no_callback_when_already_alive():
    p = _make_poller()
    p._in_game = True
    p._was_dead = False

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    p.on_death.assert_not_called()
    p.on_respawn.assert_not_called()


def test_no_callback_when_already_dead():
    p = _make_poller()
    p._in_game = True
    p._was_dead = True

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", True)]):
        p._tick()

    p.on_death.assert_not_called()
    p.on_respawn.assert_not_called()


def test_api_unavailable_triggers_game_end():
    on_game_end = MagicMock()
    p = _make_poller(on_game_end=on_game_end)
    p._in_game = True

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=None):
        p._tick()

    assert not p._in_game
    on_game_end.assert_called_once()


def test_api_unavailable_no_player_id_triggers_game_end():
    on_game_end = MagicMock()
    p = _make_poller(on_game_end=on_game_end)
    p._in_game = True

    with patch.object(p, "_get_player_id", return_value=None):
        p._tick()

    assert not p._in_game
    on_game_end.assert_called_once()


def test_fallback_to_riot_id_game_name():
    p = _make_poller()
    p._in_game = True
    p._was_dead = False
    player = {"summonerName": "", "riotIdGameName": "CoolPlayer", "isDead": True}

    with patch.object(p, "_get_player_id", return_value="CoolPlayer"), \
         patch.object(p, "_get_player_list", return_value=[player]):
        p._tick()

    p.on_death.assert_called_once()


def test_on_game_start_fires_when_game_begins():
    on_game_start = MagicMock()
    p = _make_poller(on_game_start=on_game_start)
    p._in_game = False

    with patch.object(p, "_get_player_id", return_value="TestPlayer"), \
         patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    on_game_start.assert_called_once()
    assert p._in_game
