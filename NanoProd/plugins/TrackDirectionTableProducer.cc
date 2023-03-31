// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"


class TrackDirectionTableProducer : public edm::global::EDProducer<> {
public:
  explicit TrackDirectionTableProducer(const edm::ParameterSet& iConfig)
      : ttkToken_(esConsumes(edm::ESInputTag{"", "TransientTrackBuilder"})),
        name_(iConfig.getParameter<std::string>("name")),
        src_(consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("src"))){
    produces<nanoaod::FlatTable>();
  }

  ~TrackDirectionTableProducer() override{};

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    edm::ParameterSetDescription desc;
    desc.add<edm::InputTag>("src", edm::InputTag("finalMuons"))->setComment("input muon collection");
    desc.add<std::string>("name", "Muon")->setComment("name of the muon nanoaod::FlatTable we are extending with direction at the muon system");
    descriptions.add("directionTable", desc);
  }

private:
  void produce(edm::StreamID, edm::Event&, edm::EventSetup const&) const override;

  const edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> ttkToken_;
  std::string name_;
  edm::EDGetTokenT<edm::View<pat::Muon>> src_;
};

// ------------ method called to produce the data  ------------
void TrackDirectionTableProducer::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
  // create builder for transient tracks
  const TransientTrackBuilder& tt_builder = iSetup.getData(ttkToken_);


  edm::Handle<edm::View<pat::Muon>> muons;
  iEvent.getByToken(src_, muons);

  int precision = 10;

  unsigned int ncand = muons->size();

  std::vector<float> phi_at_muonSys(ncand, 0.0);
  std::vector<float> eta_at_muonSys(ncand, 0.0);

  for (unsigned int i = 0; i < ncand; ++i) {
    const reco::Track& mu = *((*muons)[i].bestTrack());

    // create transient track from muon's track
    reco::TransientTrack tt_mu(tt_builder.build(mu));
    // define global point in the muon system
    GlobalPoint point_muonSys(0.01, 0.01, 0.01);
    // get trajectory state at surface corresponding to global point
    TrajectoryStateOnSurface traj_mu_surf = tt_mu.stateOnSurface(point_muonSys);

    phi_at_muonSys[i] = traj_mu_surf.globalMomentum().phi();
    eta_at_muonSys[i] = traj_mu_surf.globalMomentum().eta();
    std::cout << phi_at_muonSys[i] << std::endl;
  }

  auto tab = std::make_unique<nanoaod::FlatTable>(ncand, name_, false, true);

  tab->addColumn<float>("phiAtMuonSyst", phi_at_muonSys, "phi at beginning of muon system", precision);
  tab->addColumn<float>("etaAtMuonSyst", eta_at_muonSys, "eta at beginning of muon system", precision);
  iEvent.put(std::move(tab));
}


#include "FWCore/Framework/interface/MakerMacros.h"
//define this as a plug-in
DEFINE_FWK_MODULE(TrackDirectionTableProducer);
