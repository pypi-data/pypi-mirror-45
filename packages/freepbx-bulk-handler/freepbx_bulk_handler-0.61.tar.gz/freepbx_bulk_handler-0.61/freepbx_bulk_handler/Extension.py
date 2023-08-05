class Extension(object):
    """
    Write out to a CSV file to get a list of all the variables available for this class (there are too many to list
    here).
    Some "sane" defaults are set for some of the values (those that I understand what they do).
    Values 'extension' and 'name' are mandatory.
    """
    HEADER = ('extension', 'name', 'password', 'voicemail', 'ringtimer', 'noanswer', 'recording', 'outboundcid',
              'sipname', 'noanswer_cid', 'busy_cid', 'chanunavail_cid', 'noanswer_dest', 'busy_dest',
              'chanunavail_dest', 'mohclass', 'id', 'tech', 'dial', 'devicetype', 'user', 'description',
              'emergency_cid',  'recording_in_external', 'recording_out_external', 'recording_in_internal',
              'recording_out_internal', 'recording_ondemand', 'recording_priority', 'answermode', 'intercom',
              'cid_masquerade', 'concurrency_limit', 'accountcode', 'aggregate_mwi', 'allow', 'avpf', 'callerid',
              'context', 'defaultuser', 'device_state_busy_at', 'disallow', 'dtmfmode', 'force_rport', 'icesupport',
              'mailbox', 'match', 'max_contacts', 'maximum_expiration', 'media_encryption',
              'media_encryption_optimistic', 'media_use_received_transport', 'minimum_expiration', 'mwi_subscription',
              'namedcallgroup', 'namedpickupgroup', 'outbound_proxy', 'qualifyfreq', 'rewrite_contact', 'rtcp_mux',
              'rtp_symmetric', 'secret', 'sendrpid', 'sipdriver', 'timers', 'transport', 'trustrpid',
              'callwaiting_enable', 'findmefollow_strategy', 'findmefollow_grptime', 'findmefollow_grppre',
              'findmefollow_grplist', 'findmefollow_annmsg_id', 'findmefollow_postdest', 'findmefollow_dring',
              'findmefollow_needsconf', 'findmefollow_remotealert_id', 'findmefollow_toolate_id',
              'findmefollow_ringing', 'findmefollow_pre_ring', 'findmefollow_voicemail', 'findmefollow_calendar_id',
              'findmefollow_calendar_match', 'findmefollow_changecid', 'findmefollow_fixedcid', 'findmefollow_enabled',
              'voicemail_enable', 'voicemail_vmpwd', 'voicemail_email', 'voicemail_pager', 'voicemail_options',
              'voicemail_same_exten', 'disable_star_voicemail', 'vmx_unavail_enabled', 'vmx_busy_enabled',
              'vmx_temp_enabled', 'vmx_play_instructions', 'vmx_option_0_number', 'vmx_option_1_number',
              'vmx_option_2_number', 'hint_override', 'bundle')
    SPECIAL_ATTRIBUTES = ('findmefollow_postdest', 'findmefollow_grplist', 'mailbox', 'callerid', 'cid_masquerade',
                          'user', 'dial', 'id', 'voicemail', 'ringtime', 'mohclass', 'tech', 'devicetype',
                          'recording_in_external', 'recording_out_external', 'recording_in_internal',
                          'recording_out_internal', 'recording_ondemand', 'recording_priority', 'answermode',
                          'intercom', 'concurrency_limit', 'aggregate_mwi', 'avpf', 'context', 'device_state_busy_at',
                          'dtmfmode', 'force_rport', 'icesupport', 'max_contacts', 'max_expiration', 'media_encryption',
                          'media_encryption_optimistic', 'media_use_received_transport', 'minimum_expiration',
                          'mwi_subscription', 'qualifyfreq', 'rewrite_contact', 'rtcp_mux', 'rtp_symmetric', 'secret',
                          'sendrpid', 'sipdriver', 'timers', 'trustpid', 'callwaiting_enable', 'findmefollow_strategy',
                          'findmefollow_grptime', 'findmefollow_ringing', 'findmefollow_pre_ring',
                          'findmefollow_voicemail', 'findmefollow_calendar_match', 'findmefollow_changecid',
                          'voicemail_enable', 'voicemail_options', 'voicemail_same_exten', 'disable_star_voicemail',
                          'emergency_cid', 'bundle')

    def __init__(self, name: str, extension: int, **kwargs):
        self.name = name
        self.extension = extension
        for key, value in kwargs.items():
            if key in self.HEADER:
                if key in self.SPECIAL_ATTRIBUTES:
                    key = f'_{key}'
                setattr(self, key, value)
            else:
                raise ValueError(f"Key '{key}' does not exist for this class.")

    @property
    def maximum_expiration(self):
        try:
            return self._maximum_expiration
        except AttributeError:
            return f'7200'

    @property
    def disable_star_voicemail(self):
        try:
            return self._disable_star_voicemail
        except AttributeError:
            return f'yes'

    @property
    def voicemail_same_exten(self):
        try:
            return self._voicemail_same_exten
        except AttributeError:
            return f'yes'

    @property
    def voicemail_options(self):
        try:
            return self._voicemail_options
        except AttributeError:
            return f'attach=yes|saycid=no|envelope=no|delete=yes'

    @property
    def voicemail_enable(self):
        try:
            return self._voicemail_enable
        except AttributeError:
            return f'yes'

    @property
    def findmefollow_changecid(self):
        try:
            return self._findmefollow_changecid
        except AttributeError:
            return f'default'

    @property
    def findmefollow_calendar_match(self):
        try:
            return self._findmefollow_calendar_match
        except AttributeError:
            return f'yes'

    @property
    def findmefollow_voicemail(self):
        try:
            return self._findmefollow_voicemail
        except AttributeError:
            return f'default'

    @property
    def findmefollow_pre_ring(self):
        try:
            return self._findmefollow_pre_ring
        except AttributeError:
            return f'7'

    @property
    def findmefollow_ringing(self):
        try:
            return self._findmefollow_ringing
        except AttributeError:
            return f'Ring'

    @property
    def findmefollow_grptime(self):
        try:
            return self._findmefollow_grptime
        except AttributeError:
            return f'20'

    @property
    def findmefollow_annmsg_id(self):
        try:
            return self._findmefollow_annmsg_id
        except AttributeError:
            return f''

    @property
    def findmefollow_remotealert_id(self):
        try:
            return self._findmefollow_remotealert_id
        except AttributeError:
            return f''

    @property
    def findmefollow_toolate_id(self):
        try:
            return self._findmefollow_toolate_id
        except AttributeError:
            return f''

    @property
    def findmefollow_strategy(self):
        try:
            return self._findmefollow_strategy
        except AttributeError:
            return f'ringallv2-prim'

    @property
    def callwaiting_enable(self):
        try:
            return self._callwaiting_enable
        except AttributeError:
            return f'ENABLED'

    @property
    def trustpid(self):
        try:
            return self._trustpid
        except AttributeError:
            return f'yes'

    @property
    def timers(self):
        try:
            return self._timers
        except AttributeError:
            return f'yes'

    @property
    def sipdriver(self):
        try:
            return self._sipdriver
        except AttributeError:
            if self.tech == 'pjsip':
                return f'chan_pjsip'
            elif self.tech == 'sip':
                return f'chan_sip'
            else:
                return f''

    @property
    def sendrpid(self):
        try:
            return self._sendrpid
        except AttributeError:
            return f'pai'

    @property
    def secret(self):
        try:
            return self._secret
        except AttributeError:
            return f'REGEN'

    @property
    def rtp_symmetric(self):
        try:
            return self._rtp_symmetric
        except AttributeError:
            return f'yes'

    @property
    def rtcp_mux(self):
        try:
            return self._rtcp_mux
        except AttributeError:
            return f'no'

    @property
    def rewrite_contact(self):
        try:
            return self._rewrite_contact
        except AttributeError:
            return f'yes'

    @property
    def qualifyfreq(self):
        try:
            return self._qualifyfreq
        except AttributeError:
            return f'60'

    @property
    def mwi_subscription(self):
        try:
            return self._mwi_subscription
        except AttributeError:
            return f'auto'

    @property
    def minimum_expiration(self):
        try:
            return self._minimum_expiration
        except AttributeError:
            return f'60'

    @property
    def media_use_received_transport(self):
        try:
            return self._media_use_received_transport
        except AttributeError:
            return f'no'

    @property
    def media_encryption_optimistic(self):
        try:
            return self._media_encryption_optimistic
        except AttributeError:
            return f'no'

    @property
    def media_encryption(self):
        try:
            return self._media_encryption
        except AttributeError:
            return f'no'

    @property
    def max_expiration(self):
        try:
            return self._max_expiration
        except AttributeError:
            return f'7200'

    @property
    def max_contacts(self):
        try:
            return self._max_contacts
        except AttributeError:
            return f'1'

    @property
    def icesupport(self):
        try:
            return self._icesupport
        except AttributeError:
            return f'no'

    @property
    def force_rport(self):
        try:
            return self._force_rport
        except AttributeError:
            return f'yes'

    @property
    def dtmfmode(self):
        try:
            return self._dtmfmode
        except AttributeError:
            return f'rfc4733'

    @property
    def device_state_busy_at(self):
        try:
            return self._device_state_busy_at
        except AttributeError:
            return f'0'

    @property
    def context(self):
        try:
            return self._context
        except AttributeError:
            return f'from-internal'

    @property
    def avpf(self):
        try:
            return self._avpf
        except AttributeError:
            return f'no'

    @property
    def aggregate_mwi(self):
        try:
            return self._aggregate_mwi
        except AttributeError:
            return f'yes'

    @property
    def concurrency_limit(self):
        try:
            return self._concurrency_limit
        except AttributeError:
            return f'3'

    @property
    def intercom(self):
        try:
            return self._intercom
        except AttributeError:
            return f'enabled'

    @property
    def answermode(self):
        try:
            return self._answermode
        except AttributeError:
            return f'disabled'

    @property
    def recording_priority(self):
        try:
            return self._recording_priority
        except AttributeError:
            return f'10'

    @property
    def recording_ondemand(self):
        try:
            return self._recording_ondemand
        except AttributeError:
            return f'disabled'

    @property
    def recording_in_internal(self):
        try:
            return self._recording_in_internal
        except AttributeError:
            return f'dontcare'

    @property
    def recording_out_internal(self):
        try:
            return self._recording_out_internal
        except AttributeError:
            return f'dontcare'

    @property
    def recording_out_external(self):
        try:
            return self._recording_out_external
        except AttributeError:
            return f'dontcare'

    @property
    def recording_in_external(self):
        try:
            return self._recording_in_external
        except AttributeError:
            return f'dontcare'

    @property
    def devicetype(self):
        try:
            return self._devicetype
        except AttributeError:
            return f'fixed'

    @property
    def tech(self):
        try:
            return self._tech
        except AttributeError:
            return f'pjsip'

    @property
    def mohclass(self):
        try:
            return self._mohclass
        except AttributeError:
            return f'default'

    @property
    def ringtimer(self):
        try:
            return self._ringtimer
        except AttributeError:
            return f'0'

    @property
    def voicemail(self):
        try:
            return self._voicemail
        except AttributeError:
            return f'default'

    @property
    def id(self):
        try:
            return self._id
        except AttributeError:
            return f'{self.extension}'

    @property
    def dial(self):
        try:
            return self._dial
        except AttributeError:
            if self.tech:
                return f'{self.tech.upper()}/{self.extension}'
            else:
                return f'UNKNOWN/{self.extension}'

    @property
    def user(self):
        try:
            return self._user
        except AttributeError:
            return f'{self.extension}'

    @property
    def cid_masquerade(self):
        try:
            return self._cid_masquerade
        except AttributeError:
            return f'{self.extension}'

    @property
    def callerid(self):
        try:
            return self._callerid
        except AttributeError:
            return f'{self.name} <{self.extension}>'

    @property
    def mailbox(self):
        try:
            return self._mailbox
        except AttributeError:
            return f'{self.extension}@device'

    @property
    def findmefollow_grplist(self):
        try:
            return self._findmefollow_grplist
        except AttributeError:
            return f'{self.extension}'

    @property
    def findmefollow_postdest(self):
        try:
            return self._findmefollow_postdest
        except AttributeError:
            return f'ext-local,{self.extension},dest'

    @property
    def to_dict(self):
        return {
            key: getattr(self, key, None)
            for key in self.HEADER
        }

    @property
    def emergency_cid(self):
        try:
            return self._emergency_cid
        except AttributeError:
            return f'{self.name}'

    @property
    def bundle(self):
        try:
            return self._bundle
        except AttributeError:
            return 'no'

