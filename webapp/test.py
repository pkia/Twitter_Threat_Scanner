def test_database():
    
    db.drop_all()
    db.create_all()

    account_1 = Account(id="john123", name="John")
    account_2 = Account(id="john12345", name="John 2")
    db.session.add(account_1)
    db.session.add(account_2)

    
    report_1 = Report(threat_type="racism",summary="he was mean to me", account_id=account_1.id)
    report_2 = Report(threat_type="racism",summary="she was very mean to me", account_id=account_2.id)
    
    scan_1 = ScanResult(id="123456", threat_detected="racism", threat_level=9, account_id=account_1.id)
    scan_2 = ScanResult(id="1234", threat_detected="racism", threat_level=5, account_id=account_2.id)
    
    db.session.add(report_1)
    db.session.add(report_2)
    db.session.add(scan_1)
    db.session.add(scan_2)
    
    db.session.commit()

    Account.query.all()


test_database()
