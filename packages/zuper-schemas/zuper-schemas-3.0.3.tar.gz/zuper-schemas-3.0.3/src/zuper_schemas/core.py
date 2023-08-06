from .utils import dataclass, Generic

# @dataclass
# class ConcreteResult:  # no jobs in side
#     content: Any
#
#
# @dataclass
# class ConcreteCallable:
#     pass
#
#
# @dataclass
# class LocalPythonFunction(ConcreteCallable):
#     python_function: str
#
#
# @dataclass
# class FunctionCall:
#     callable: FunctionDefinition
#     parameters: Dict[str, Any]
#
#     def __call__(self, **kwargs):
#         callable = ExpectFunctionDefinition(implementations={}, function_call=self)
#         return FunctionCall(callable=callable, parameters=kwargs)
#
# #
# @dataclass
# class ExpectFunctionDefinition(FunctionDefinition):
#     function_call: FunctionCall
#
# @dataclass
# class Node:
#     pass
#
# @dataclass
# class CurrentNode(Node):
#     pass
#
# @dataclass
# class Context:
#     node: Node
#     time: float
#
#
# def lookup_from_context(*, context: Context, identifier: str) -> Context:
#     pass
#
#
# def F(f):
#     assert isinstance(f, Callable), f
#     f0 = FunctionDefinition(implementations={'python': LocalPythonFunction(python_function=f.__name__)})
#
#     def f2(*args, **kwargs):
#         if args:
#             msg = 'Cannot call this with positional arguments: %s %s' % (f, args)
#             raise TypeError(msg)
#         return FunctionCall(callable=f0, parameters=kwargs)
#
#     return f2
#
#
# def zuper_link_resolve(*, context: Context, link: IPDELink) -> Any:
#     if '/' in link:
#         i = link.index('/')
#         first = link[:i]
#         rest = link[i + 1]
#     else:
#         first = link
#         rest = IPDELink('')
#
#     context2 = F(lookup_from_context)(context=context, identifier=first)
#
#     if rest:
#         return F(zuper_link_resolve)(context=context2, link=rest)
#     else:
#         return context2
#
#
# class DNS:
#     pass
#
#
# def lookup(*, context: Context, first: Identifier, rest: str = None):
#     rest = rest or []
#     dns_lookup = F(zuper_link_resolve)(context=context, link=IPDELink("@Instance/api/dns/lookup"))
#     resolved = dns_lookup(domain=first, record="txt")
#     return F(zuper_link_resolve)(context=resolved, link=rest)
#
# def zm_resolve_callable(link) -> Callable:
#     pass
#
#
# class LookupInterface:
#     def __call__(self, domain: Domain, record: str) -> Optional[str]:
#         return ''
#
# def lookup(domain: Domain, origin: Node, time: Timespec ):
#     dns_lookup: LookupInterface = zm_resolve_callable("@Instance/api/dns/lookup")
#
#     record = dns_lookup(domain=domain, record='txt')
#
#
#
# class Root:
#     ipde = 0






# @Executable:
#
# @Executable/Python:
#
# @Executable/Program:
#    docker: @DockerExecution
#
#
# @Alert:
#    message:
#    location?:
#
# @Alert/Warning:
#
# @Alert/Error:
#
#
# @JobResult:
#   job: @Job
#   warnings: @list(@Warning)
#
#   console_output: @ConsoleOutput
#
# @ConsoleOutput:
#    stderr: @ConsoleOutputStream
#    stdout: @ConsoleOutputStream
#
# @ConsoleOutputStream:
#    previous?: @ConsoleOutputStream
#    line: @bytes
#
#
# @JobResult/EvaluationFailure:
#
#
# @JobResult/Success:
#    result: @
#
# @JobResult/Failure:
#    errors: @list(@Errors)
#
# @JobResult/Failure/PartialFailure:
#    partial_result: @

#######
#
#@TypedData:
#  size: @int
#  mime_type: @string
#  encoding: @string

###########
#
# @IPCLSegment:
#
# @IPCLSegment:Resolution:
#
#
# @IPCLSegment:IPNSSegment:
#   ipns: @multihash
#
# @IPCL:
#   elements: @list(IPCLSegment)
#
# @Link:
#
# @Link/ZuperLink:
#   Cid: @cid
#   IsData: @bool
#   IsMeta: @bool
#   IsHistory: @bool
#   CurrentMetaSize: @int
#   HistoryMetaSize: @int
#   CurrentDataSize: @int
#   HistoryDataSize: @int
#
# @Link:LinkToIPCL:
#   ipcl: @IPCL
#   type:
#
# @Link:LinkToVersion:
#   entity: @Entity
#   value: @
#
# @Link:LinkToJob:
#   job: @Job
#   expect-shape: @Shape
#
# @Link:LinkToJobResult:
#   job_result: @JobResult
#   expect-shape: @Shape
#
# @HashResult:
#   algorithm: @string
#   results: @bytes
#
# @AES_Encrypted:
#   payload: @TypedData # with mime=der
#   key-hash: @HashResult
#
# @SecretSharedKey:
#   key-hash: @HashResult
#   plain: @bytes
#
# @EncryptedFor:
#   dest: @PublicKey
#   payload: @bytes
#
# @PublicKey:
#   content: @TypedData
#   private?: @PrivateKey
#
# @PrivateKey:
#   content: @TypedData
#
# @SignedEnvelope:
#   data: @
#   signature: @Signature
#
# @Signature:
#   key: @PublicKey
#   result: @bytes
#
#
# @ClockReference:
#
#
#
# # published at public key
# @ArbiterInfo:
#   keys: @dict(QueueInfo)
#
# @QueueInfo:
#   last: @VersionInfo # link to last version
#   queues: @list(Queue)
#
# @Queue:Pubsub:
#   topic: @string
#
# @Queue:Websocket:
#   url: @url
#
