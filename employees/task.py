
# from .models import EmplpyeePoints, EmplpyeePointsHour

# def update_something():
#     print("updating employe points every hour")
#     points = EmplpyeePoints.objects.all()

#     for p in points:
#         EmplpyeePointsHour.objects.create(
#             name = p.name,
#             total = p.total,
#             new_order = p.new_order,
#             complete_order = p.complete_order,
#             return_order = p.return_order,
#             ad_note = p.ad_note,
#             rtn_note = p.rtn_note,
#             search = p.search,
#             misc = p.misc,
#         )
#         p.name = p.name
#         p.total = 0
#         p.new_order = 0
#         p.complete_order = 0
#         p.return_order = 0
#         p.ad_note = 0
#         p.rtn_note = 0
#         p.search = 0
#         p.misc = 0

#         p.save()
