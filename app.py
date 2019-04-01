import dbase
import pandas as pd

def fetch(user_id):
	dbcon = None
	try:
		dbcon = dbase.get_connection()
		query = '''SELECT (CASE WHEN feed_type_id = 1 THEN REPLACE(JSON_EXTRACT(summary_json, '$.title'), '"', '') WHEN feed_type_id = 2 THEN wp.title WHEN feed_type_id = 3 THEN wc.title WHEN feed_type_id = 4 THEN ws.title END) title, wdfsi.feed_id, wfcm.channel_id, (CASE WHEN social_interaction_type_id = 1 THEN COUNT(wdfsi.doc_id) * 0.6 WHEN social_interaction_type_id = 2 THEN COUNT(wdfsi.doc_id) WHEN social_interaction_type_id = 3 THEN COUNT(DISTINCT wdfsi.doc_id) * 0.3 + share_view_count * 0.2 WHEN social_interaction_type_id = 4 THEN COUNT(DISTINCT wdfsi.doc_id) * 0.3 END) score, COUNT(DISTINCT wdfsi.doc_id) user_count FROM wc_feed wf JOIN wc_doc_feed_social_interaction wdfsi ON wf.feed_id = wdfsi.feed_id JOIN tbl_doc_profile tdp ON wdfsi.doc_id = tdp.doc_id JOIN wc_doc_speciality wds ON tdp.doc_id = wds.doc_id JOIN wc_feed_channel_mapping wfcm ON wdfsi.feed_id = wfcm.feed_id JOIN (SELECT DISTINCT feed_id FROM wc_doc_feed_social_interaction WHERE doc_id != {}) vf ON wfcm.feed_id = vf.feed_id JOIN (SELECT channel_id FROM wc_doc_channel_subscription WHERE doc_id = {}) wdcs ON wfcm.channel_id = wdcs.channel_id JOIN (SELECT speciality_id FROM wc_doc_speciality WHERE doc_id = {}) wds1 ON wds.speciality_id = wds1.speciality_id LEFT JOIN wc_article wa ON wf.feed_id = wa.feed_id LEFT JOIN wc_case wc ON wf.feed_id = wc.feed_id LEFT JOIN wc_post wp ON wf.feed_id = wp.feed_id LEFT JOIN wc_survey ws ON wf.feed_id = ws.feed_id GROUP BY wdfsi.feed_id , wds.speciality_id HAVING score > 5 AND user_count > 10 ORDER BY wdfsi.created_date DESC, user_count DESC , score DESC;'''
		with dbcon.cursor() as cursor:
			cursor.execute(query.format(user_id, user_id, user_id))
			rows = cursor.fetchall()
			df = pd.DataFrame(rows)
			df.to_csv('collab-filter.csv')
	except Exception as e:
		print(str(e))
	finally:
		if dbcon: dbcon.close()

def read():
	df = pd.read_csv('collab-filter.csv')
	print(df.head(10))

if __name__ == '__main__':
	fetch(4)
	read()