# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import statutils


def count_answer_user(qset=None, measures=None, period=None):
    if qset is None:
        qset = models.Answer.objects.all()
    qset = statutils.using_stats_db(qset)
    dstat = statutils.DateStat(qset, 'create_time')
    funcs = {
        'today': lambda: dstat.stat("今天", count_field="user_id", distinct=True, only_first=True),
        'yesterday': lambda: dstat.stat("昨天", count_field="user_id", distinct=True, only_first=True),
        'all': lambda: qset.values("user_id").distinct().count(),
        'daily': lambda: dstat.stat(period, count_field='user_id', distinct=True),
        'clazz': lambda: statutils.count_by(
            dstat.get_period_query_set(period),
            'user__as_school_student__clazz__name',
            count_field='user_id',
            distinct=True, sort="-"),
        'course': lambda: statutils.count_by(
            dstat.get_period_query_set(period).filter(paper__course_courses__isnull=False),
            "paper__course_courses__name",
            count_field='user_id',
            distinct=True, sort="-"),
        'chapter': lambda: statutils.count_by(
            dstat.get_period_query_set(period).filter(paper__course_chapters__isnull=False),
            "paper__course_chapters__name",
            count_field='user_id',
            distinct=True, sort="-")
    }
    return dict([(m, funcs[m]()) for m in measures])
