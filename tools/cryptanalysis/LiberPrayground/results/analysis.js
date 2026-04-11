var MIN_IOC = 0;
var MAX_IOC = 0;
var MIN_CHR = 0;
var MAX_CHR = 0;

function byID(x) { return document.getElementById(x); }

function loadFile(url, callback, async=true) {
	var xobj = new XMLHttpRequest();
	// xobj.overrideMimeType('text/plain');
	xobj.open('GET', url, async);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == '200') {
			callback(xobj.responseText);
		}
	};
	xobj.send(null);
}

function load_from_file() {
	const fname = byID('fileload').value;
	loadFile('../pages/' + fname + '.txt', function(res) {
		if (!res) { res = 'Error loading file.'; }
		byID('input').value = res;
		start_analyze();
	});
}

function dt_dd(title, content, clss = '', id = '') {
	var attr = '';
	if (id != '') { attr += ' id="' + id + '"'; }
	if (clss != '') { attr += ' class="' + clss + '"'; }
	return '<dt>' + title + '</dt>\n<dd' + attr + '>\n' + content + '</dd>\n';
}

function num_stream(stream) {
	var txt = '';
	for (var i = 0; i < stream.length; i++) {
		var val = stream[i];
		var title = '';
		const typ = typeof stream[i];
		if (typ != 'string' && typ != 'number') {
			title = ' title="' + val[1] + '"';
			val = val[0];
		}
		txt += '<div' + title + '>' + val + '</div>';
	}
	return txt + '\n';
}

function ngram_table(rows, id, th = null) {
	var txt = '<table id="' + id + '">\n';
	txt += '<tr>';
	if (th != null) { txt += '<th></th>'; }
	for (var i = 0; i < window.txt_abc.length; i++) {
		txt += '<th>' + window.txt_abc[i] + '</th>';
	}
	if (th == null) { th = ['']; }
	txt += '</tr>\n';
	for (var o = 0; o < th.length; o++) {
		txt += '<tr>';
		if (th[o] != '') { txt += '<th>' + th[o] + '</th>'; }
		for (var i = 0; i < window.txt_abc.length; i++) {
			const key = th[o] + window.txt_abc[i];
			const val = rows[key] || '';
			const title = val ? ' title="' + key + '"' : '';
			txt += '<td' + title + '>' + val + '</td>';
		}
		txt += '</tr>\n';
	}
	txt += '</table>\n';
	return txt;
}

function apply_colors(tableid, tag, low = null, high = null) {
	var nodes = byID(tableid).querySelectorAll(tag);
	if (low == null || high == null) {  // either both or none
		low = 9999;
		high = 0;
		for (var i = 0; i < nodes.length; i++) {
			const tt = nodes[i].innerHTML;
			if (tt == '' || tt == '–' || tt == '.' || tt == 'NaN') { continue; }
			const val = Number(tt);
			if (val > high) { high = val; }
			if (val < low) { low = val; }
		}
	}
	for (var i = 0; i < nodes.length; i++) {
		const tt = nodes[i].innerHTML;
		if (tt == '' || tt == '–' || tt == '.' || tt == 'NaN') { continue; }
		var x = Number(tt);
		var clss = 0;
		if (x > low) {
			if (x > high) { x = high; }
			clss = parseInt((x - low) / (high - low) * 14) + 1
		}
		nodes[i].classList = ['m' + clss];
	}
}

function pick_ngrams(c, grams, limit) {
	var items = Object.keys(grams).map(function(key) {
		return [key, grams[key]];
	});
	items.sort(function(fst, snd) { return snd[1] - fst[1]; });
	const select = items.slice(0, limit);
	var z = '';
	for (var i = 0; i < select.length; i++) {
		z += '<div><div>' + select[i][0] + ':</div> ' + select[i][1] + '</div>';
	}
	if (items.length > limit) {
		z += '+' + (items.length - limit) + '&nbsp;others'
	}
	return dt_dd(c + '-grams:', z, 'tabwidth');
}

function sec_counts() {
	var ngrams = [];
	for (var s = 0; s < 4; s++) {
		var arrset = {};
		for (var i = 0; i < window.runes.length - s; i++) {
			var key = window.runes[i];
			for (var u = 0; u < s; u++) {
				key += window.runes[i + u + 1];
			}
			arrset[key] = (arrset[key] || 0) + 1;
		}
		ngrams.push(arrset);
	}
	var txt = '<p><b>Letters:</b> ' + window.runes.length + '</p>\n';
	txt += '<p><b>Words:</b> ' + window.words.length + '</p>\n';
	txt += '<dl>\n';
	var wlens = [];
	for (var i = 0; i < window.words.length; i++) {
		wlens.push([window.words[i].length, window.words[i] + ' (' + window.eng_words[i].join('') + ')']);
	}
	txt += dt_dd('Word lengths:', num_stream(wlens), 'ioc-list small two', 'strm-wlen');
	txt += dt_dd('1-grams:', ngram_table(ngrams[0], 'tbl-1g'));
	txt += dt_dd('2-grams:', ngram_table(ngrams[1], 'tbl-2g', window.txt_abc));
	txt += pick_ngrams(3, ngrams[2], 100);
	txt += pick_ngrams(4, ngrams[3], 50);
	txt += '</dl>\n';
	byID('sec_counts').innerHTML = txt;
	apply_colors('strm-wlen', 'div');
	apply_colors('tbl-1g', 'td');
	apply_colors('tbl-2g', 'td');
}

function IC_direct(prob, count) {
	var sum = 0;
	var ioc = 0;
	for (k in prob) {
		sum += prob[k];
		ioc += prob[k] * (prob[k] - 1);
	}
	return ioc / ((sum * (sum - 1)) / count);
}

function count_table(id, nums) {
	var counts = [];
	var high = 0;
	for (var i = nums.length - 1; i >= 0; i--) {
		const val = nums[i][0];
		if (val > high) { high = val; }
		counts[val] = (counts[val] || 0) + 1;
	}
	var txt = '<table id="' + id + '">\n<tr>';
	for (var i = 0; i <= high; i++) { txt += '<th>' + i + '</th>'; }
	txt += '</tr>\n<tr>';
	for (var i = 0; i <= high; i++) { txt += '<td>' + (counts[i] || '–') + '</td>'; }
	txt += '</tr>\n</table>\n';
	// txt += '<br><span class="small">⤳ IoC: ' + IC_direct(counts, high + 1).toFixed(3) + '</span>';
	return txt;
}

function sec_double() {
	var num_a = [];
	var num_b = [];
	var num_c = [];
	for (var i = 0; i < window.runes.length - 1; i++) {
		const a = window.txt_abc.indexOf(window.runes[i]);
		const b = window.txt_abc.indexOf(window.runes[i + 1]);
		const c = window.txt_abc.indexOf(window.runes[i + 2]);
		const x = (b - a + window.txt_abc.length) % window.txt_abc.length;
		num_a.push(x == 0  ? [1, 'offset: ' + i + ', char: ' + window.txt_abc[a]] : '.');
		num_b.push([x, 'offset: ' + i]);
		if (c != -1) {  // is -1 for the last entry
			const y = (c - a + window.txt_abc.length) % window.txt_abc.length;
			num_c.push([y, 'offset: ' + i]);
		}
	}
	var num_vig_b = [];
	var num_vig_c = [];
	for (var i = 0; i < num_b.length; i++) {
		num_vig_b.push(window.txt_abc[num_b[i][0]]);
	}
	for (var i = 0; i < num_c.length; i++) {
		num_vig_c.push(window.txt_abc[num_c[i][0]]);
	}
	var txt = '';
	txt += dt_dd('Double Letters:', num_stream(num_a), 'ioc-list small one', 'strm-dbls');
	txt += dt_dd('Letter Difference (2nd – 1st):', num_stream(num_b), 'ioc-list small two', 'strm-diff2a');
	txt += dt_dd('Count Difference (2nd – 1st):', count_table('tbl-ldiff2a', num_b));
	txt += dt_dd('IoC Difference (2nd – 1st):', keylen_table('tbl-kldiff2', ['IoC'], [num_vig_b], 1, 18));
	for (var i = num_b.length - 1; i >= 0; i--) {
		num_b[i][0] = Math.min(num_b[i][0], window.txt_abc.length - num_b[i][0])
	}
	txt += dt_dd('Letter Difference (2nd, Absolute):', num_stream(num_b), 'ioc-list small two', 'strm-diff2b');
	txt += dt_dd('Count Difference (2nd, Absolute):', count_table('tbl-ldiff2b', num_b));

	txt += dt_dd('Letter Difference (3rd – 1st):', num_stream(num_c), 'ioc-list small two', 'strm-diff3a');
	txt += dt_dd('Count Difference (3rd – 1st):', count_table('tbl-ldiff3a', num_c));
	txt += dt_dd('IoC Difference (3rd – 1st):', keylen_table('tbl-kldiff3', ['IoC'], [num_vig_c], 1, 18));
	for (var i = num_c.length - 1; i >= 0; i--) {
		num_c[i][0] = Math.min(num_c[i][0], window.txt_abc.length - num_c[i][0])
	}
	txt += dt_dd('Letter Difference (3rd, Absolute):', num_stream(num_c), 'ioc-list small two', 'strm-diff3b');
	txt += dt_dd('Count Difference (3rd, Absolute):', count_table('tbl-ldiff3b', num_c));
	
	byID('sec_double').innerHTML = '<dl>\n' + txt + '</dl>\n';
	apply_colors('strm-dbls', 'div', 0, 1);
	for (var i = 2; i <= 3; i++) {
		apply_colors('strm-diff' + i + 'a', 'div', 0, window.txt_abc.length - 1);
		apply_colors('strm-diff' + i + 'b', 'div', 0, parseInt((window.txt_abc.length - 1) / 2));
		apply_colors('tbl-ldiff' + i + 'a', 'td');
		apply_colors('tbl-ldiff' + i + 'b', 'td');
		apply_colors('tbl-kldiff' + i, 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
		apply_colors('tbl-kldiff' + i, 'tr.small>td', MIN_CHR, MAX_CHR);
	}
}

function IC(nums) {
	var prob = {};
	for (var i = nums.length - 1; i >= 0; i--) {
		prob[nums[i]] = (prob[nums[i]] || 0) + 1;
	}
	var ioc = 0;
	for (k in prob) { ioc += prob[k] * (prob[k] - 1); }
	return ioc / ((nums.length * (nums.length - 1)) / window.txt_abc.length);
}

function mod_str(text, mod) {
	var groups = [];
	for (var i = mod; i > 0; i--) { groups.push(''); }
	for (var i = 0; i < text.length; i++) {
		groups[i % mod] += text[i];
	}
	return groups;
}

function IC_w_keylen(text, keylen) {
	if (text.length < 2 * keylen) { return NaN; }
	const groups = mod_str(text, keylen);
	var ioc = 0;
	for (var i = groups.length - 1; i >= 0; i--) {
		ioc += IC(groups[i]);
	}
	return Number(ioc / keylen).toFixed(2);
}

function IC_w_kl_pattern(text, keylen, pattern) {
	if (text.length < 2 * keylen) { return NaN; }
	var groups = [];
	for (var i = keylen; i > 0; i--) { groups.push(''); }
	for (var i = 0; i < text.length; i++) {
		groups[pattern[i]] += text[i];
	}
	var ioc = 0;
	for (var i = groups.length - 1; i >= 0; i--) {
		ioc += IC(groups[i]);
	}
	return Number(ioc / keylen).toFixed(2);
}

function keylen_table(id, titles, parts, from = 1, to = 16) {
	var txt = '<table id="' + id + '">\n';
	txt += '<tr><th>keylen</th>';
	for (var i = from; i <= to; i++) { txt += '<th>' + i + '</th>'; }
	txt += '</tr>\n';
	for (var p = 0; p < parts.length; p++) {
		txt += '<tr><th>' + titles[p] + '</th>';
		for (var kl = from; kl <= to; kl++) {
			txt += '<td>' + IC_w_keylen(parts[p], kl) + '</td>';
		}
		txt += '</tr>\n';
	}
	txt += '<tr class="small"><th>chr / keylen</th>';
	for (var kl = from; kl <= to; kl++) {
		txt += '<td>' + parseInt(parts.slice(-1)[0].length / kl) + '</td>'
	}
	txt += '</tr>\n</table>\n';
	return txt;
}

function sec_ioc() {
	const tbl_a = keylen_table('tbl-ioc-1', ['IoC'], [window.runes], 1, 16);
	const tbl_b = keylen_table('tbl-ioc-2', ['IoC'], [window.runes], 17, 32);
	byID('sec_ioc').innerHTML = tbl_a + '<br>' + tbl_b;
	apply_colors('tbl-ioc-1', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-1', 'tr.small>td', MIN_CHR, MAX_CHR);
	apply_colors('tbl-ioc-2', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-2', 'tr.small>td', MIN_CHR, MAX_CHR);
}

function sec_ioc_mod() {
	var txt = '<dl>\n';
	for (var mod = 2; mod <= 3; mod++) {
		const groups = mod_str(window.runes, mod);
		var titles = [];
		for (var i = 0; i < mod; i++) {
			titles.push('x%' + mod + ' == ' + i);
		}
		const tbl = keylen_table('tbl-ioc-mod' + mod, titles, groups, 2, 18);
		txt += dt_dd('Modulo ' + mod, tbl);
	}
	byID('sec_ioc_mod').innerHTML = txt + '</dl>\n';
	apply_colors('tbl-ioc-mod2', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-mod2', 'tr.small>td', MIN_CHR, MAX_CHR);
	apply_colors('tbl-ioc-mod3', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-mod3', 'tr.small>td', MIN_CHR, MAX_CHR);
}

function pattern_mirror_table() {
	var txt = '<table id="tbl-ioc-pattern-mirror">\n';
	txt += '<tr><th>keylen</th>';
	for (var i = 4; i <= 18; i++) { txt += '<th>' + i + '</th>'; }
	txt += '</tr>\n';
	txt += '<tr><th>Type A</th>';
	for (var kl = 4; kl <= 18; kl++) {
		var pattern = [];
		for (var i = 0; i < window.runes.length; i++) {
			var ki = i % (kl * 2);
			if (ki >= kl) { ki = kl * 2 - 1 - ki; }
			pattern.push(ki);
		}
		txt += '<td>' + IC_w_kl_pattern(window.runes, kl, pattern) + '</td>';
	}
	txt += '</tr>\n';
	txt += '<tr><th>Type B</th>';
	for (var kl = 4; kl <= 18; kl++) {
		var pattern = [];
		for (var i = 0; i < window.runes.length; i++) {
			var ki = i % (kl * 2 - 2);
			if (ki >= kl) { ki = kl * 2 - 2 - ki; }
			pattern.push(ki);
		}
		txt += '<td>' + IC_w_kl_pattern(window.runes, kl, pattern) + '</td>';
	}
	txt += '</tr>\n';
	txt += '<tr class="small"><th>chr / keylen</th>';
	for (var kl = 4; kl <= 18; kl++) {
		txt += '<td>' + parseInt(window.runes.length / kl) + '</td>'
	}
	return txt + '</tr>\n</table>\n';
}

function pattern_shift_table() {
	var txt = '<table id="tbl-ioc-pattern-shift">\n';
	txt += '<tr><th>keylen</th>';
	for (var i = 4; i <= 18; i++) { txt += '<th>' + i + '</th>'; }
	txt += '</tr>\n';
	for (var shift = 0; shift <= 17; shift++) {
		txt += '<tr><th>&lt;&lt;' + shift + '</th>';
		for (var kl = 4; kl <= 18; kl++) {
			if (shift >= kl) {
				txt += '<td>–</td>';
				continue;
			}
			var pattern = [];
			for (var i = 0; i < window.runes.length; i++) {
				pattern.push((i + shift * parseInt(i / kl)) % kl);
			}
			txt += '<td>' + IC_w_kl_pattern(window.runes, kl, pattern) + '</td>';
		}
		txt += '</tr>\n';
	}
	txt += '<tr class="small"><th>chr / keylen</th>';
	for (var kl = 4; kl <= 18; kl++) {
		txt += '<td>' + parseInt(window.runes.length / kl) + '</td>'
	}
	return txt + '</tr>\n</table>\n';
}

function sec_ioc_pattern() {
	var txt = '<dl>\n';
	txt += dt_dd('Mirror Pattern', pattern_mirror_table());
	txt += dt_dd('Shift Pattern', pattern_shift_table());
	byID('sec_ioc_pattern').innerHTML = txt + '</dl>\n';
	apply_colors('tbl-ioc-pattern-mirror', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-pattern-mirror', 'tr.small>td', MIN_CHR, MAX_CHR);
	apply_colors('tbl-ioc-pattern-shift', 'tr:not(.small)>td', MIN_IOC, MAX_IOC);
	apply_colors('tbl-ioc-pattern-shift', 'tr.small>td', MIN_CHR, MAX_CHR);
}

function sec_ioc_flow() {
	const wsize = [20, 30, 50, 80, 120];
	txt = '<dl>\n'
	for (var i = 0; i < 5; i++) {
		var nums = [];
		for (var o = 0; o <= window.runes.length - wsize[i]; o++) {
			const sub = window.runes.slice(o, o + wsize[i]);
			nums.push([IC(sub).toFixed(2), 'offset: ' + o]);
		}
		txt += dt_dd('Window size ' + wsize[i] + ':', num_stream(nums), 'ioc-list small four', 'strm-ioc-flow-' + wsize[i]);
	}
	byID('sec_ioc_flow').innerHTML = txt + '</dl>\n';
	for (var i = 0; i < 5; i++) {
		apply_colors('strm-ioc-flow-' + wsize[i], 'div', MIN_IOC - 0.1, MAX_IOC);
	}
}

function ioc_head(desc, letters) {
	return desc + ' (IoC: ' + IC(letters).toFixed(3) + '):';
}

function sec_conceal() {
	var txt = '';
	for (var n = 1; n <= 8; n++) {
		txt += '<h3>Pick every ' + n + '. word</h3>\n<dl>\n';
		for (var u = 0; u < n; u++) {
			if (n > 1) {
				txt += '<h4>Start with ' + (u + 1) + '. word</h4>\n';
			}
			var subwords = '';
			var subrunes = [];
			var subfirst = [];
			var sublast = [];
			for (var i = u; i < window.eng_words.length; i += n) {
				const word = window.eng_words[i];
				for (var w = 0; w < word.length; w++) {
					subwords += word[w];
				}
				subwords += ' ';
				subrunes = subrunes.concat(word);
				subfirst.push(word[0]);
				sublast.push(word[word.length - 1]);
			}
			txt += dt_dd(ioc_head('Words', subrunes), subwords);

			for (var i = 0; i < 2; i++) {
				const letters = [subfirst, sublast][i];
				const desc = ['first', 'last'][i];
				var divarr = '';
				for (var o = 0; o < letters.length; o++) {
					divarr += '<div>' + letters[o] + '</div>';
				}
				txt += dt_dd(ioc_head('Pick every ' + desc + ' letter', letters), divarr, 'runelist');
			}
		}
		txt += '</dl>\n'
	}
	byID('sec_conceal').innerHTML = txt;
}

function start_analyze() {
	window.txt_abc = byID('abc').value;
	var abc_123 = {};
	var trans = byID('abc_123').value.trim().split(' ');
	if (trans.length == 0 || trans.length == 1 && !trans[0]) {
		trans = window.txt_abc;
	} else if (trans.length != window.txt_abc.length) {
		alert('Alphabet and translation length mismatch! (' + window.txt_abc.length + ' vs. ' + trans.length + ')');
		return;
	}
	for (var i = trans.length - 1; i >= 0; i--) {
		abc_123[window.txt_abc[i]] = trans[i];
	}
	window.txt_src = byID('input').value;
	const no_nl = byID('chk_nonl').checked;
	var words = ' ';
	var runes = '';
	for (var i = 0; i < window.txt_src.length; i++) {
		const letter = window.txt_src[i];
		if (window.txt_abc.includes(letter)) {
			runes += letter;
			words += letter;
		} else if (no_nl && letter == '\n') {
			continue;
		} else if (words.slice(-1) != ' ') {
			words += ' '
		}
	}
	window.runes = runes;
	window.words = words.trim().split(' ');
	var eng_words = [];
	for (var i = 0; i < window.words.length; i++) {
		const word = window.words[i];
		var this_word = [];
		for (var u = 0; u < word.length; u++) {
			this_word.push(abc_123[word[u]]);
		}
		eng_words.push(this_word);
	}
	window.eng_words = eng_words;
	MIN_CHR = parseInt(window.txt_abc.length * 0.9);
	MAX_CHR = parseInt(window.txt_abc.length * 3);
	MIN_IOC = parseFloat(byID('ioc_min').value || byID('ioc_min').placeholder);
	MAX_IOC = parseFloat(byID('ioc_max').value || byID('ioc_max').placeholder);
	sec_counts();
	sec_double();
	sec_ioc();
	sec_ioc_mod();
	sec_ioc_pattern();
	sec_ioc_flow();
	sec_conceal();
}
