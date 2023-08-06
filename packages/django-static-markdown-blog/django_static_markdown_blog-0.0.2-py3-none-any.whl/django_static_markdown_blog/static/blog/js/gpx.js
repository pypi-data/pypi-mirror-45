
function get_duration_string(duration) {
  var s = '';

  if (duration >= _DAY_IN_MILLIS) {
    s += Math.floor(duration / _DAY_IN_MILLIS) + ' jours';
  }

  if (duration >= _HOUR_IN_MILLIS) {
    s += Math.floor(duration / _HOUR_IN_MILLIS) + 'h';
    duration = duration % _HOUR_IN_MILLIS
  }

  var mins = Math.floor(duration / _MINUTE_IN_MILLIS);
  duration = duration % _MINUTE_IN_MILLIS;
  if (mins < 10) s+= '0';
  s += mins + 'm';

  var secs = Math.floor(duration / _SECOND_IN_MILLIS);
  if (secs < 10) s += '0';
  s += secs + 's';

  return s;
}

function display_gpx(elt, marker_options) {
  if (!elt) return;

  var url = elt.getAttribute('data-gpx-source');
  var mapid = elt.getAttribute('data-map-target');
  if (!url || !mapid) return;

  function _t(t) { return elt.getElementsByTagName(t)[0]; }
  function _c(c) { return elt.getElementsByClassName(c)[0]; }

  var map = L.map(mapid);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://www.osm.org">OpenStreetMap</a>'
  }).addTo(map);

  new L.GPX(url, {
    async: true,
    marker_options: marker_options,
  }).on('loaded', function(e) {
    var gpx = e.target;
    map.fitBounds(gpx.getBounds());

    _t('h3').textContent = gpx.get_name();
    _c('start').textContent = gpx.get_start_time().toLocaleString();
    _c('distance').textContent = gpx.m_to_km(gpx.get_distance()).toFixed(2);
    _c('duration').textContent = get_duration_string(gpx.get_moving_time());
    _c('elevation-gain').textContent = gpx.get_elevation_gain().toFixed(0);
    _c('elevation-loss').textContent = gpx.get_elevation_loss().toFixed(0);
    _c('elevation-net').textContent  = (gpx.get_elevation_gain() - gpx.get_elevation_loss()).toFixed(0);
    
    var speed = gpx.get_moving_speed();
    if (speed > 10)
        _c('average-speed').textContent = speed.toFixed(0);
    else
        _c('average-speed').textContent = speed.toFixed(2);

    var stop_time = gpx.get_total_time() - gpx.get_moving_time();
    _c('stop-duration').textContent = get_duration_string(gpx.get_total_time() - gpx.get_moving_time());
  }).addTo(map);
}
