#!/usr/bin/env python3
"""Family Sports Photo Desk — brief-050 / 060 / 066 / 081 / 084 — 127.0.0.1:4329 only."""
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", 4329))

BRIEFS_FOLDED = ["brief-050", "brief-060", "brief-066", "brief-081", "brief-084"]

BLOCKED050 = [
    "/api/auto-post-photos",
    "/api/fabricate-album",
    "/api/auto-share-album",
    "/api/kids-public-post",  # overlap → prefer 066 when also in BLOCKED066; 081 for album gates
    "/api/auto-upload-cloud",  # overlap → prefer 066
]
BLOCKED060 = [
    "/api/auto-post-film",
    "/api/fabricate-clip-count",
    "/api/auto-airdrop-film",
    "/api/auto-upload-film",
    "/api/kids-public-film",
    "/api/fake-live-clip-board",
    # auto-share-reel + auto-text-kids overlap → prefer 066 / 081
]
BLOCKED066 = [
    "/api/auto-post-reel",
    "/api/fabricate-reel",
    "/api/auto-share-reel",
    "/api/auto-upload-cloud",
    "/api/kids-public-post",
    "/api/exif-gps-leak",
    "/api/fake-live-reel-board",
    "/api/auto-text-kids",
    "/api/auto-airdrop-reel",
    "/api/hold-timeout-post",
    "/api/auto-airplay-reel",
    "/api/faces-public-without-hold",
    "/api/reel/auto-post",
    "/api/reel/auto-share",
]
# Carpool photo-day dual-Hold gates — prefer brief-081 body
BLOCKED081 = [
    "/api/auto-text-kids",
    "/api/auto-post-photos",
    "/api/fabricate-album",
    "/api/auto-notify-drivers",
    "/api/auto-share-album",
    "/api/auto-assign-coverage",
    "/api/auto-airdrop",
    "/api/fake-live-album",
    "/api/hold-timeout-notify",
    "/api/burn-outbound",
    # aliases peers may probe
    "/api/carpool/auto-notify",
    "/api/carpool/auto-assign",
    "/api/carpool/auto-text-kids",
    "/api/album/auto-share",
    "/api/album/auto-post",
    "/api/photo/auto-share",
]
# Film-room Sunday share gates — prefer brief-084 body
BLOCKED084 = [
    "/api/auto-post-film",
    "/api/auto-text-kids",
    "/api/fabricate-clip-count",
    "/api/auto-send-slack",
    "/api/auto-airdrop",
    "/api/fabricate-leave-by",
    "/api/auto-share-reel",
    "/api/fake-live-clips",
    "/api/hold-timeout-share",
    "/api/burn-outbound",
    # aliases peers may probe
    "/api/filmroom/auto-post",
    "/api/filmroom/auto-share",
    "/api/filmroom/auto-text",
    "/api/filmroom/auto-slack",
    "/api/filmroom/auto-airdrop",
    "/api/filmroom/fake-live",
    "/api/clips/auto-share",
    "/api/clips/fabricate-count",
]

OVERLAP_ALSO_066 = {
    "/api/auto-share-reel": ["brief-060", "brief-084"],  # if ever hit (084 prefers)
    "/api/auto-upload-cloud": ["brief-050", "brief-060"],
    "/api/kids-public-post": ["brief-050", "brief-060"],
    "/api/auto-text-kids": ["brief-060", "brief-081", "brief-084"],  # if ever hit (084 prefers)
}

OVERLAP_ALSO_081 = {
    "/api/auto-text-kids": ["brief-066", "brief-060", "brief-023", "brief-084"],  # if ever hit (084 prefers)
    "/api/auto-post-photos": ["brief-050", "brief-066"],
    "/api/fabricate-album": ["brief-050"],
    "/api/auto-share-album": ["brief-050"],
    "/api/auto-airdrop": ["brief-050", "brief-060", "brief-066", "brief-084"],  # if ever hit (084 prefers)
    "/api/fake-live-album": ["brief-050", "brief-066"],
    "/api/hold-timeout-notify": ["brief-066", "brief-060"],
    "/api/burn-outbound": ["brief-050", "brief-060", "brief-066", "brief-023", "brief-084"],
    "/api/auto-notify-drivers": ["brief-023"],
    "/api/auto-assign-coverage": ["brief-023"],
    "/api/carpool/auto-notify": ["brief-023"],
    "/api/carpool/auto-assign": ["brief-023"],
    "/api/carpool/auto-text-kids": ["brief-066", "brief-060", "brief-023", "brief-084"],
    "/api/album/auto-share": ["brief-050"],
    "/api/album/auto-post": ["brief-050", "brief-066"],
    "/api/photo/auto-share": ["brief-050"],
}

OVERLAP_ALSO_084 = {
    "/api/auto-post-film": ["brief-060", "brief-050", "brief-066", "brief-081"],
    "/api/auto-text-kids": ["brief-081", "brief-066", "brief-060", "brief-050"],
    "/api/fabricate-clip-count": ["brief-060", "brief-050", "brief-066", "brief-081"],
    "/api/auto-send-slack": ["brief-050", "brief-060", "brief-066", "brief-081"],
    "/api/auto-airdrop": ["brief-081", "brief-050", "brief-060", "brief-066"],
    "/api/fabricate-leave-by": ["brief-050", "brief-060", "brief-081"],
    "/api/auto-share-reel": ["brief-066", "brief-060", "brief-050", "brief-081"],
    "/api/fake-live-clips": ["brief-060", "brief-066", "brief-050", "brief-081"],
    "/api/hold-timeout-share": ["brief-066", "brief-060", "brief-050", "brief-081"],
    "/api/burn-outbound": ["brief-081", "brief-050", "brief-060", "brief-066"],
    "/api/filmroom/auto-post": ["brief-060", "brief-050", "brief-066", "brief-081"],
    "/api/filmroom/auto-share": ["brief-050", "brief-060", "brief-066", "brief-081"],
    "/api/filmroom/auto-text": ["brief-081", "brief-066", "brief-060", "brief-050"],
    "/api/filmroom/auto-slack": ["brief-050", "brief-060", "brief-066", "brief-081"],
    "/api/filmroom/auto-airdrop": ["brief-081", "brief-050", "brief-060", "brief-066"],
    "/api/filmroom/fake-live": ["brief-060", "brief-066", "brief-050", "brief-081"],
    "/api/clips/auto-share": ["brief-050", "brief-060", "brief-066", "brief-081"],
    "/api/clips/fabricate-count": ["brief-060", "brief-050", "brief-066", "brief-081"],
}


def brief050():
    d = json.load(open(os.path.join(HERE, "data", "brief050.json")))
    d["live_check"] = {
        "albums_live": False,
        "example_only": True,
        "scorecard_all_zero": all(v == 0 for v in d["scorecard"].values()),
    }
    return d


def brief060():
    d = json.load(open(os.path.join(HERE, "data", "brief060.json")))
    d["live_check"] = {
        "clips_live": False,
        "example_only": True,
        "scorecard_all_zero": all(v == 0 for v in d["scorecard"].values()),
    }
    return d


def brief066():
    d = json.load(open(os.path.join(HERE, "data", "brief066.json")))
    sc = d["scorecard"]
    d["live_check"] = {
        "ok": True,
        "fake_live": 0,
        "reel_live": False,
        "example_only": True,
        "scorecard_all_zero": all(v == 0 for v in sc.values()),
        "fabricate_reel": sc.get("fabricate_reel", 0),
        "auto_post_reel": sc.get("auto_post_reel", 0),
    }
    return d


def brief081():
    d = json.load(open(os.path.join(HERE, "data", "brief081.json")))
    sc = d["scorecard"]
    board = dict(d.get("carpool_photo_day") or {})
    album = dict(board.get("album") or {})
    album["live_badge"] = False
    album["proof"] = None
    album["count"] = None
    if album.get("status") == "LIVE" and not album.get("proof"):
        album["status"] = "EXAMPLE"
    album.setdefault("status", "EXAMPLE")
    carpool = dict(board.get("carpool") or {})
    carpool["proof"] = None
    carpool.setdefault("status", "EXAMPLE")
    carpool.setdefault("roster", [])
    carpool.setdefault("drivers", [])
    holds = dict(board.get("holds") or {})
    for key in ("notify_drivers", "share_album"):
        h = dict(holds.get(key) or {})
        h.setdefault("state", "HOLD")
        h.setdefault("default", "review_private")
        h["destination"] = h.get("destination") or "review_private"
        h["digest_sha256"] = None
        h["expires_at"] = None
        holds[key] = h
    board["album"] = album
    board["carpool"] = carpool
    board["holds"] = holds
    board["dual_proof"] = False
    board["honesty"] = "EXAMPLE/SYNTHETIC"
    d["carpool_photo_day"] = board
    d["live_check"] = {
        "ok": True,
        "fake_live": 0,
        "albums_live": False,
        "dual_proof": False,
        "example_only": True,
        "scorecard_all_zero": all(v == 0 for v in sc.values()),
        "auto_text_kids": sc.get("auto_text_kids", 0),
        "auto_post_photos": sc.get("auto_post_photos", 0),
        "fabricate_album": sc.get("fabricate_album", 0),
        "auto_notify_drivers": sc.get("auto_notify_drivers", 0),
        "auto_share_album": sc.get("auto_share_album", 0),
        "auto_assign_coverage": sc.get("auto_assign_coverage", 0),
        "auto_airdrop": sc.get("auto_airdrop", 0),
        "fake_live_album": sc.get("fake_live_album", 0),
        "hold_timeout_notify": sc.get("hold_timeout_notify", 0),
        "burn_outbound": sc.get("burn_outbound", 0),
        "album_count": None,
        "merge_apply": False,
        "cousins": d.get("cousins") or {},
        "holds": holds,
        "honesty": "EXAMPLE/SYNTHETIC — album counts null until file proof; dual_proof=false; Hold review_private",
    }
    return d


def brief084():
    d = json.load(open(os.path.join(HERE, "data", "brief084.json")))
    sc = d["scorecard"]
    board = dict(d.get("film_room_sunday") or {})
    clips = dict(board.get("clips") or {})
    clips["live_badge"] = False
    clips["proof"] = None
    clips["count"] = None
    if clips.get("status") == "LIVE" and not clips.get("proof"):
        clips["status"] = "EXAMPLE"
    clips.setdefault("status", "EXAMPLE")
    leave = dict(board.get("leave_by") or {})
    leave["live_badge"] = False
    leave["basis"] = None
    leave["time"] = None
    if leave.get("status") == "LIVE" and not leave.get("basis"):
        leave["status"] = "EXAMPLE"
    leave.setdefault("status", "EXAMPLE")
    holds = dict(board.get("holds") or {})
    for key in ("share", "text_kids"):
        h = dict(holds.get(key) or {})
        h.setdefault("state", "HOLD")
        h.setdefault("default", "review_private")
        h["destination"] = h.get("destination") or "review_private"
        h["digest_sha256"] = None
        h["expires_at"] = None
        holds[key] = h
    board["clips"] = clips
    board["leave_by"] = leave
    board["holds"] = holds
    board["dual_proof"] = False
    board["honesty"] = "EXAMPLE/SYNTHETIC"
    d["film_room_sunday"] = board
    d["live_check"] = {
        "ok": True,
        "fake_live": 0,
        "clips_live": False,
        "dual_proof": False,
        "example_only": True,
        "scorecard_all_zero": all(v == 0 for v in sc.values()),
        "auto_post_film": sc.get("auto_post_film", 0),
        "auto_text_kids": sc.get("auto_text_kids", 0),
        "fabricate_clip_count": sc.get("fabricate_clip_count", 0),
        "auto_send_slack": sc.get("auto_send_slack", 0),
        "auto_airdrop": sc.get("auto_airdrop", 0),
        "fabricate_leave_by": sc.get("fabricate_leave_by", 0),
        "auto_share_reel": sc.get("auto_share_reel", 0),
        "fake_live_clips": sc.get("fake_live_clips", 0),
        "hold_timeout_share": sc.get("hold_timeout_share", 0),
        "burn_outbound": sc.get("burn_outbound", 0),
        "clip_count": None,
        "leave_by": None,
        "merge_apply": False,
        "cousins": d.get("cousins") or {},
        "holds": holds,
        "honesty": (
            "EXAMPLE/SYNTHETIC — clip counts null until file proof; dual_proof=false; "
            "Hold review_private before Slack/share/text; cousins 050/060/066/081 merge_apply=false"
        ),
    }
    return d



def health():
    return {
        "ok": True,
        "app": "family-sports-photo-desk",
        "port": PORT,
        "host": "127.0.0.1",
        "timezone": "America/New_York",
        "briefs_folded": list(BRIEFS_FOLDED),
    }


class H(BaseHTTPRequestHandler):
    def send(s, c, b, t="application/json"):
        b = b.encode()
        s.send_response(c)
        s.send_header("Content-Type", t)
        s.send_header("Content-Length", str(len(b)))
        s.send_header("Cache-Control", "no-store")
        s.end_headers()
        s.wfile.write(b)

    def refuse066(s, p):
        body = {
            "ok": False,
            "error": "forbidden by brief-066 (Hold before share/post; human Apply only; never fabricate LIVE reel)",
            "brief": "brief-066",
            "path": p,
            "also_refused_by": OVERLAP_ALSO_066.get(p, []),
            "message": (
                "Family sports highlight reel law (brief-066). "
                "auto_post_reel=0 / fabricate_reel=0. Compile private; "
                "Hold before share/post/AirDrop/AirPlay/cloud; EXIF strip; "
                "LIVE length only with file proof."
            ),
        }
        return s.send(403, json.dumps(body))

    def refuse081(s, p):
        body = {
            "ok": False,
            "error": "forbidden by brief-081 (carpool+photo dual Hold; human Apply only; never fabricate LIVE album)",
            "brief": "brief-081",
            "brief_id": "brief-081",
            "path": p,
            "also_refused_by": OVERLAP_ALSO_081.get(p, []),
            "merge_apply": False,
            "message": (
                "Family sports carpool photo-day Hold (brief-081). "
                "auto_text_kids=0 · auto_post_photos=0 · fabricate_album=0. "
                "Hold before notify drivers or share album; dual_proof=false; "
                "cousin brief-023/050/060/066 merge_apply=false (notify ≠ share ≠ coverage). "
                "Not KPD. America/New_York."
            ),
        }
        return s.send(403, json.dumps(body))

    def refuse084(s, p):
        body = {
            "ok": False,
            "error": "forbidden by brief-084 (film-room Sunday Hold; human Apply only; never fabricate LIVE clips)",
            "brief": "brief-084",
            "brief_id": "brief-084",
            "path": p,
            "also_refused_by": OVERLAP_ALSO_084.get(p, []),
            "merge_apply": False,
            "message": (
                "Family sports film-room Sunday Hold (brief-084). "
                "auto_post_film=0 · auto_text_kids=0 · fabricate_clip_count=0. "
                "Hold before Slack share / kids text / AirDrop / reel share; "
                "clip counts null until dual_proof; leave-by EXAMPLE without basis; "
                "cousin brief-050/060/066/081 merge_apply=false "
                "(photo share ≠ film-night ≠ film-room share ≠ carpool notify). "
                "Not KPD. America/New_York."
            ),
        }
        return s.send(403, json.dumps(body))

    def route(s):
        p = s.path.split("?")[0]
        # Prefer brief-084 on film-room Sunday share gates
        if p in BLOCKED084:
            return s.refuse084(p)
        # Prefer brief-081 on carpool-photo dual-Hold gates (unique stubs kept)
        if p in BLOCKED081:
            return s.refuse081(p)
        # Prefer brief-066 refuse (with also_refused_by) on reel overlaps
        if p in BLOCKED066:
            return s.refuse066(p)
        if p in BLOCKED050:
            return s.send(
                403,
                json.dumps(
                    {
                        "error": "forbidden by brief-050 (Hold before share; human Apply only)",
                        "brief": "brief-050",
                        "also_refused_by": ["brief-081"] if p in (
                            "/api/auto-post-photos",
                            "/api/fabricate-album",
                            "/api/auto-share-album",
                        ) else [],
                        "path": p,
                    }
                ),
            )
        if p in BLOCKED060:
            return s.send(
                403,
                json.dumps(
                    {
                        "error": "forbidden by brief-060 (film Hold before share; human Apply only)",
                        "brief": "brief-060",
                        "path": p,
                    }
                ),
            )
        if s.command != "GET":
            return s.send(404, '{"error":"not found"}')
        if p == "/api/brief050":
            return s.send(200, json.dumps(brief050(), indent=2))
        if p == "/api/brief060":
            return s.send(200, json.dumps(brief060(), indent=2))
        if p == "/api/brief066":
            return s.send(200, json.dumps(brief066(), indent=2))
        if p == "/api/brief081":
            return s.send(200, json.dumps(brief081(), indent=2))
        if p == "/api/brief084":
            return s.send(200, json.dumps(brief084(), indent=2))
        if p in ("/healthz", "/api/health", "/health"):
            return s.send(200, json.dumps(health(), indent=2))
        if p in ("/", "/index.html"):
            return s.send(
                200,
                open(os.path.join(HERE, "web", "index.html")).read(),
                "text/html; charset=utf-8",
            )
        s.send(404, '{"error":"not found"}')

    do_GET = do_POST = do_PUT = do_DELETE = route

    def log_message(s, *a):
        pass


if __name__ == "__main__":
    print(f"http://127.0.0.1:{PORT}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
