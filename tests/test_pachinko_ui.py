from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PachinkoUiRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / "src" / "pachinko_ui.py").read_text(encoding="utf-8")
        cls.app = (ROOT / "app.py").read_text(encoding="utf-8")

    def test_result_card_omits_qr_and_webapp_url(self):
        self.assertNotIn("x.drawImage(qr,1460,brandY-30,82,82)", self.source)
        self.assertNotIn("qr_data_json", self.source)
        self.assertIn("const footerY=800,footerHeight=", self.source)
        self.assertIn("PLAY DATE ／ プレイ日時", self.source)
        self.assertNotIn("ACHIEVEMENTS ／ 獲得称号", self.source)
        self.assertNotIn('class="rc-qr"', self.source)
        self.assertNotIn('id="playResultQr"', self.source)
        self.assertNotIn("<div class=\"rc-brand\">", self.source)
        self.assertNotIn('<h2>RESULT CARD</h2>', self.source)

    def test_pity_time_display_remains_null_aware_without_online_registration(self):
        self.assertIn("initial===null?'--.---':Number(initial).toFixed(3)", self.source)
        self.assertNotIn("async function registerRanking()", self.source)
        self.assertNotIn("pachinko_results", self.source)
        self.assertNotIn("SB_KEY", self.source)

    def test_pity_demo_button_and_sample_mode_are_removed(self):
        self.assertNotIn('id="pityTest"', self.source)
        self.assertNotIn('runPityDemo', self.source)
        self.assertNotIn('demoMode', self.source)

    def test_initial_spec_percentages_and_display_probability(self):
        for value in ('約26.9%', '約55.8%', '約15.4%', '約1.9%'):
            self.assertIn(value, self.source)
        self.assertIn('通常大当たり確率：52/1,799（約1/34.6）', self.source)
        self.assertIn('50回転連続未当たりで時短へ移行', self.source)
        self.assertIn('時短は131回転', self.source)
        self.assertIn('時短中の大当たり期待度：約97.9％', self.source)
        self.assertIn('6,000 NOTES</span><b>100%</b>', self.source)

    def test_expected_values_are_integer_display_values(self):
        for value in ('1,465 NOTES', '1,520 NOTES', '8,511 NOTES', '10,030 NOTES'):
            self.assertIn(value, self.source)

    def test_rush_payout_table_uses_matching_colors(self):
        for value in ('#399cff', '#e6bd43', '#e85c86', '#ff5c78', '#a987ff'):
            self.assertIn(value, self.source)

    def test_hold_trust_and_appearance_rates_are_displayed(self):
        for value in ('約0.5%', '約3%', '約60%', '約85%', '100%', '90%', '9%', '0.9%', '0.09%', '0.01%'):
            self.assertIn(value, self.source)

    def test_rush_remaining_spin_phases_are_defined(self):
        for value in ('CHANCE ZONE', 'HIGH CHANCE', 'COUNT DOWN', 'FINAL CHANCE'):
            self.assertIn(value, self.source)
        self.assertIn('if(st>=31)', self.source)
        self.assertIn('if(st>=11)', self.source)
        self.assertIn('if(st>=6)', self.source)
        self.assertIn('if(st>=2)', self.source)

    def test_achievements_are_added_to_result_and_share(self):
        for value in ('RUSH MASTER', 'RUSH LEGEND', 'PREMIUM', 'TIME MODE', 'OVERALL KING', 'HIGH ROLLER', 'QUICK START', 'LAST MOMENT', 'RAINBOW'):
            self.assertIn(value, self.source)
        self.assertNotIn('獲得称号 ／ ACHIEVEMENTS', self.source)
        self.assertIn('function achievementList()', self.source)

    def test_effect_mode_is_fixed_to_premium(self):
        self.assertIn('selectedMode="PREMIUM"', self.source)
        self.assertNotIn('id="effectMode"', self.source)
        self.assertNotIn('function modeDescription(mode)', self.source)
        self.assertIn("document.body.dataset.mode='premium'", self.source)

    def test_confirmed_jackpot_has_mode_specific_rainbow_and_pity_is_separate(self):
        self.assertIn("async function jackpotEffect(d,prize,isInitial=false)", self.source)
        self.assertIn("screen.classList.add('jackpot-'+mode.toLowerCase())", self.source)
        self.assertIn("number.classList.add('rainbowFlash')", self.source)
        self.assertIn("function visualPayout()", self.source)
        self.assertIn("function visualRandom()", self.source)
        self.assertIn("crypto.getRandomValues(a)", self.source)
        self.assertIn("const winning=String(Math.floor(visualRandom()*10)).repeat(3)", self.source)
        self.assertIn("className='number pityFlash'", self.source)
        self.assertIn("classList.add('time-entry','pity-burst')", self.source)

    def test_result_card_does_not_use_fixed_4_3_clipping(self):
        self.assertNotIn("aspect-ratio:4/3", self.source)
        self.assertIn("overflow:visible", self.source)

    def test_pachinko_online_ranking_is_removed(self):
        self.assertNotIn('OVERALL PACHINKO 総獲得NOTESランキング', self.app)
        self.assertNotIn('fetch_pachinko_ranking', self.app)
        self.assertNotIn('pachinko_rank_page', self.app)
        self.assertNotIn('registerRanking()', self.source)

    def test_simulation_histogram_runs_from_f_to_sss_plus_without_downloads(self):
        self.assertIn('rank_order = [item["rank"] for item in reversed(simulation_summary["histogram"])]', self.app)
        self.assertIn('st.bar_chart(hist_df.set_index("RANK")[["割合(%)"]], horizontal=False)', self.app)
        self.assertNotIn('download_button(', self.app[self.app.index('### 📊 100万件シミュレーション'):])
        self.assertNotIn('st.dataframe(hist_df', self.app)


    def test_result_card_uses_one_million_simulation_percentile(self):
        self.assertIn('SIMULATION ／ 100万件中の位置', self.source)
        self.assertIn('function topPercentile(totalNotes)', self.source)
        self.assertIn('item.total_notes)>=Number(totalNotes)', self.source)
        self.assertIn('上位${value.toFixed(1)}%', self.source)
        self.assertIn('simulation_distribution=simulation_distribution', self.app)
        self.assertNotIn('RANKING ／ 総合評価ランキング', self.source)
        self.assertNotIn('未接続（ランキング機能は未接続です）', self.source)


    def test_one_million_simulation_distribution_supports_percentile_calculation(self):
        summary_path = ROOT / "output" / "simulation" / "pachinko_simulation_1m_summary.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        distribution = summary["total_notes_distribution"]
        self.assertEqual(summary["count"], 1_000_000)
        self.assertEqual(sum(int(item["count"]) for item in distribution), summary["count"])
        score = 29_100
        count_at_or_above = sum(int(item["count"]) for item in distribution if int(item["total_notes"]) >= score)
        self.assertEqual(count_at_or_above, 55_384)
        self.assertEqual(round(count_at_or_above / summary["count"] * 100, 1), 5.5)

    def test_live_rank_progress_and_rush_spin_counter_are_present(self):
        for value in ('id="rankProgress"', 'id="currentRank"', 'id="nextRankText"', 'id="rankProgressBar"', 'id="rushSpinCount"'):
            self.assertIn(value, self.source)
        self.assertIn("次のRANK", self.source)
        self.assertIn("RANK F まで", self.source)

    def test_final_14_spins_have_slow_tempo_bgm_and_special_hit(self):
        self.assertIn("function startFinalBgm()", self.source)
        self.assertIn("function stopFinalBgm()", self.source)
        self.assertIn("const finalPhase=st<=10||st===0", self.source)
        self.assertIn("consumeTimer=setInterval(consume,1900)", self.source)
        self.assertIn("if(finalPhase)", self.source)
        self.assertIn("ST本体の最後10回転（107～116回転目）と残保留4個", self.source)

    def test_requested_main_hero_title_is_restored(self):
        self.assertIn('TAP TIMING ANALYZER', self.app)
        self.assertIn('あんさんぶるスターズ！！Music</div>', self.app)
        self.assertIn('タップタイミング解析</div>', self.app)

    def test_mobile_game_controls_are_after_number_and_stats(self):
        screen=self.source.index('<div class="screen" id="screen">')
        stats=self.source.index('<div class="stats">')
        mode=self.source.index('<div class="normalModeSelect" id="normalModePanel">')
        rank=self.source.index('<div class="rank-progress" id="rankProgress">')
        self.assertLess(screen, stats)
        self.assertLess(stats, mode)
        self.assertLess(mode, rank)
        self.assertIn("$('currentRank').className='rank-'+rankColor(current[1])", self.source)

    def test_manual_describes_rush_as_continuation_mode_not_higher_hit_rate(self):
        self.assertIn('連チャン（継続）を狙う特別な遊技状態・モード', self.source)
        self.assertNotIn('RUSHは通常時より大当たりしやすい特別な状態です', self.source)

    def test_one_push_rainbow_and_win_sound_start_together(self):
        self.assertIn("screen.classList.add('rush-special-win');playTone(48,.24,'sawtooth',.11);const winSound=specialWinSound('ONE_PUSH')", self.source)

    def test_shadow_visitor_eyes_are_high_intensity_red(self):
        self.assertIn('#ff183eaa', self.source)
        self.assertIn('drop-shadow(0 0 14px #ff123f)', self.source)

    def test_manual_uses_accordions_without_chapter_navigation_buttons(self):
        self.assertNotIn('<nav class="manual-nav">', self.source)
        self.assertIn('class="manual-chapter"', self.source)
        self.assertIn('当選信頼度', self.source)
        self.assertIn('RANKは総獲得NOTESに応じた固定評価です。', self.source)
        self.assertNotIn('ブラックアウト：画面を暗くして数字などを見えなくする演出。', self.source)
        self.assertNotIn('Q. RANKとランキングの違いは何ですか？', self.source)

    def test_x_share_uses_real_line_breaks(self):
        self.assertIn('function xWeightedLength(text)', self.source)
        self.assertIn('function fitXText(lines)', self.source)
        self.assertIn('const limit=220', self.source)
        self.assertIn('weighted>220', self.source)
        self.assertIn('const t=fitXText(lines)', self.source)



    def test_rush_presentation_modes_are_separate_from_draw_logic(self):
        self.assertIn('value="SHADOW"', self.source)
        self.assertIn('value="IMPACT"', self.source)
        self.assertIn('value="ONE_PUSH"', self.source)
        self.assertIn("function rushModeDescription(mode)", self.source)
        self.assertIn("async function rushSpecialPresentation(hit)", self.source)
        self.assertIn("shouldShowSpecialEvent(currentHoldColor,hit)", self.source)
        self.assertIn("P(hit | event)=40%", self.source)
        self.assertIn("specialWinSound(mode)", self.source)
        self.assertIn("currentHoldColor=color", self.source)

    def test_chain_escalation_thresholds_are_presentation_only(self):
        self.assertIn("rushHits>=12?'12-plus':rushHits>=8?'8-11':rushHits>=4?'4-7':'1-3'", self.source)
        self.assertIn("CHAIN ${rushHits}", self.source)
        self.assertIn("body[data-chain=\"12-plus\"]", self.source)

    def test_visual_normal_spin_does_not_consume_game_rng(self):
        self.assertIn("(60+visualRandom()*40).toFixed(3)", self.source)



    def test_payout_tiers_have_presentation_only_reveal_classes(self):
        for payout in (300, 1500, 3000, 4500, 6000):
            self.assertIn(f"payout-{payout}", self.source)
        self.assertIn("screen.classList.add('payout-'+prize)", self.source)


    def test_normal_time_has_dedicated_presentation_modes(self):
        self.assertIn('id="normalMode"', self.source)
        self.assertIn('value="STANDARD"', self.source)
        self.assertIn('value="FORESHADOW"', self.source)
        self.assertIn('value="QUICK"', self.source)
        self.assertIn("function normalModeDescription(mode)", self.source)
        self.assertIn("async function normalSpinPresentation(isHit)", self.source)

    def test_normal_time_presentation_uses_visual_rng_only(self):
        start=self.source.index("async function normalSpinPresentation(isHit)")
        end=self.source.index("function rushModeDescription(mode)", start)
        sequence=self.source[start:end]
        self.assertIn("const r=visualRandom()", sequence)
        self.assertNotIn("Math.random()", sequence)
        self.assertNotIn("weighted(", sequence)
        self.assertIn("await normalSpinPresentation(Boolean(initialTriple))", self.source)

    def test_normal_time_has_staged_tease_reach_and_final_visuals(self):
        for css_class in ("normal-tease", "normal-reach", "normal-hot", "normal-final"):
            self.assertIn(css_class, self.source)
        self.assertIn("const pace=mode==='QUICK'?.58:mode==='FORESHADOW'?1.28:1", self.source)
        self.assertNotIn("保留に気配", self.source)
        self.assertNotIn("小さな違和感", self.source)
        self.assertNotIn("虹色の光が拡大", self.source)

    def test_normal_mode_copy_and_narration_cleanup(self):
        for text in (
            'STANDARD：演出をバランスよく楽しむ王道モード。',
            'FORESHADOW：演出をじっくり楽しむモード。',
            'QUICK：変動を短くし、テンポよく楽しむモード。',
        ):
            self.assertIn(text, self.source)
        for obsolete in ('BLUE_MISS', '気配がする。', '保留に気配。', '変動開始——', 'こちらを見ている。', '小さな違和感。', '保留変化の兆し', '虹色の光が拡大！', '保留昇格！'):
            self.assertNotIn(obsolete, self.source)

    def test_rush_selector_explains_conditional_confidence(self):
        self.assertIn('専用演出（煽りを含む）の大当たり信頼度：<b>40%</b>', self.source)
        self.assertIn('SHADOW VISITOR：暗闇に潜む気配と襲来の予兆で、当落の瞬間を楽しむ告知モード。', self.source)
        self.assertIn('IMPACT：強烈な閃光と衝撃で、当落の瞬間を楽しむ一発告知モード。', self.source)
        self.assertIn('ONE PUSH：ボタンを押すその瞬間まで結果が分からない、任意タイミング解放モード。', self.source)

    def test_special_event_rates_are_separate_from_game_hit_rates(self):
        import sys
        sys.path.insert(0, str(ROOT / "src"))
        from pachinko import COLOR_HIT_RATES, SPECIAL_EVENT_RATES
        self.assertEqual(set(SPECIAL_EVENT_RATES), {"blue", "green", "red", "gold"})
        hold_mix = {"blue": .90, "green": .09, "red": .009, "gold": .0009, "rainbow": .0001}
        overall_hit = sum(w * COLOR_HIT_RATES[c] for c, w in hold_mix.items())
        overall_event = sum(hold_mix[c] * SPECIAL_EVENT_RATES.get(c, 0) for c in hold_mix)
        self.assertAlmostEqual(overall_hit, 1/73)
        self.assertAlmostEqual(overall_event, .0192735)
        for color, q in SPECIAL_EVENT_RATES.items():
            p = COLOR_HIT_RATES[color]
            self.assertLessEqual(q * .40 / p, 1)
            self.assertLessEqual(q * .60 / (1-p), 1)
            event_hit = p * (q * .40 / p)
            event_miss = (1-p) * (q * .60 / (1-p))
            self.assertAlmostEqual(event_hit / (event_hit + event_miss), .40)

    def test_yutime_countdown_and_rush_special_trust_are_documented_in_ui(self):
        self.assertIn('id="pityCountdown"', self.source)
        self.assertIn('pityLeft>PITY_SPINS', self.source)
        self.assertIn('pityLeft<=10', self.source)
        self.assertIn('大当たり信頼度を40%', self.source)
        self.assertNotIn('60%は外れ', self.source)
        self.assertNotIn('60%はずれ', self.source)


if __name__ == "__main__":
    unittest.main()
