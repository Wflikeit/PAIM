# """Containers module."""
#
# from dependency_injector import containers
#
#
# from dependency_injector import containers, providers
#
#
#
# class Container(containers.DeclarativeContainer):
#     wiring_config = containers.WiringConfiguration(
#         modules=[
#             "PAIM.infrastructure.api.endpoints.auth_router",
#             "PAIM.infrastructure.api.endpoints.client_router",
#             "PAIM.infrastructure.api.endpoints.product_router",
#
#         ]
#     )
#
#     db_session = providers.Factory(create_db_session)
#
#     unit_of_work = providers.Factory(
#         ProductService,
#         db_session,
#     )
#
#     module_service = providers.Factory(
#         ModuleService,
#         unit_of_work,
#     )
#
#     progress_service = providers.Factory(
#         ProgressService,
#         unit_of_work,
#     )
#
#     user_service = providers.Factory(
#         UserService,
#         unit_of_work,
#     )
#
#     push_client = providers.Factory(ExpoPushClient)
#
#     push_sender = providers.Factory(
#         PushNotificationSender,
#         unit_of_work,
#         push_client,
#     )
#
#     purchase_service = providers.Factory(
#         PurchaseService,
#         unit_of_work,
#     )
#
#     authenticator = providers.Factory(Authenticator)
#
#     ranking_retriever = providers.Factory(
#         RankingRetrieverMongo,
#         db_session,
#     )
#
#     ranking_evaluator = providers.Factory(
#         RankingEvaluator,
#         ranking_retriever,
#     )
#
#     heart_renewal_service = providers.Factory(
#         HeartRenewalService,
#         unit_of_work,
#     )
#
#     challenge_repo = providers.Factory(
#         ChallengeRepositoryMongo,
#         db_session,
#     )
#
#     challenge_service = providers.Factory(
#         ChallengeService,
#         challenge_repo,
#     )
#
#     modules_loader = providers.Factory(
#         FileSystemModulesLoader,
#         unit_of_work,
#     )
