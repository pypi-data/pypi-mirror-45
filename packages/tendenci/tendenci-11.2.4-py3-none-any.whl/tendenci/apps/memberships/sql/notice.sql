INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b5','Membership Join Auto Responder','0','attimeof','join','1','Membership Application for {{ first_name }} {{ last_name }}','html','Thank you for applying for membership with  {{ sitedisplayname }}. The details of your membership follow:<br><br>Name: <b>{{ first_name }} {{ last_name }}</b><br>Email: <b>{{ email }}</b><br><br>The following membership number was assigned to you: <br>Member Number: <b>{{ membernumber }}</b><br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b6','Membership Renewal Auto Responder','0','attimeof','renewal','1','Membership Renew','html','Thank you for renewing membership with  {{ sitedisplayname }}. The details of your membership follow:<br><br>Name: <b>{{ first_name }} {{ last_name }}</b><br>Email: <b>{{ email }}</b><br><br>The following membership number was assigned to you: <br>Member Number: <b>{{ membernumber }}</b><br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b7','Membership Renewal Reminder 30 Days before Expiration','30','before','expiration','1','Membership Renewal Reminder 30 Days before Expiration','html','Greetings {{ first_name }}:<br><br>Your membership with {{ sitedisplayname }} will expire in <b>30</b> days<br><br>To renew your membership go to {{ renewlink }}<br><br>To view the details of your membership go to {{ membershiplink }}<br><br>Membership Renewal Reminder from: {{ sitedisplayname }}<br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b8','Membership Renewal Reminder 14 Days before Expiration','14','before','expiration','1','Membership Renewal Reminder 14 Days before Expiration','html','Greetings {{ first_name }}:<br><br>Your membership with {{ sitedisplayname }} will expire in <b>14</b> days<br><br>To renew your membership go to {{ renewlink }}<br><br>To view the details of your membership go to {{ membershiplink }}<br><br>Membership Renewal Reminder from: {{ sitedisplayname }}<br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b9','Membership Renewal Reminder 7 Days before Expiration','7','before','expiration','1','Membership Renewal Reminder 7 Days before Expiration','html','Greetings {{ first_name }}:<br><br>Your membership with {{ sitedisplayname }} will expire in <b>7</b> days<br><br>To renew your membership go to {{ renewlink }}<br><br>To view the details of your membership go to {{ membershiplink }}<br><br>Membership Renewal Reminder from: {{ sitedisplayname }}<br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
INSERT INTO `memberships_notice` (`create_dt`,`update_dt`, `guid`, `notice_name`, `num_days`, `notice_time`, `notice_type`, `system_generated`, `subject`, `content_type`, `email_content`, `status`, `status_detail`) VALUES ('2011-03-22 15:43:12','2011-03-22 15:43:12','0aff6db0-54c4-11e0-a21d-001aa06701b1','Membership Renewal Reminder 1 Days after Expiration','1','after','expiration','1','Membership Renewal Reminder 1 Days after Expiration','html','Greetings {{ first_name }}:<br><br>Your membership with {{ sitedisplayname }} has expired.<br><br>To renew your membership go to {{ renewlink }}<br><br>To view the details of your membership go to {{ membershiplink }}<br><br>Membership Renewal Reminder from: {{ sitedisplayname }}<br><br>Thanks!<br><br>{{ sitecontactname }}<br>{{ sitecontactemail }}<br>{{ sitedisplayname }}<br>Time submitted: {{ timesubmitted }}<br>','1','active');
